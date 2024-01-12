from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from .forms import ImageForm
from .models import Image
from sklearn.cluster import KMeans
import cv2
import numpy as np
from django.utils import timezone
from .filters import ImageFilter

# Create your views here.
def palette(file_path):
    src_image = cv2.imread(file_path)
    src_image = cv2.cvtColor(src_image, cv2.COLOR_BGR2RGB)
    reshape_img = src_image.reshape((src_image.shape[0] * src_image.shape[1], 3))

    cluster = KMeans(n_clusters=10).fit(reshape_img)
    C_centroids = cluster.cluster_centers_

    C_labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    (C_hist, _) = np.histogram(cluster.labels_, bins=C_labels)
    C_hist = C_hist.astype("float")
    C_hist /= C_hist.sum()

    img_colors = sorted(
        [(percent, color) for (percent, color) in zip(C_hist, C_centroids)],
        reverse=True
    )
    return img_colors

def image_list(request):
    images = Image.objects.all().order_by('-created_date')

    my_filter = ImageFilter(request.GET, queryset=images)
    images = my_filter.qs

    paginator = Paginator(images, 35)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'my_filter': my_filter
    }
    return render(request, 'images/image_list.html', context)

def image_details(request, pk):
    image = get_object_or_404(Image, pk=pk)

    admin = False
    if request.user.groups.filter(name="Admin").exists():
        admin = True

    palitra = palette(image.content.url[1::])

    dominant_color_HEX = "#{:02x}{:02x}{:02x} ".format(int(palitra[0][1][0]), int(palitra[0][1][1]), int(palitra[0][1][2])) + "{:0.2f}%".format(palitra[0][0] * 100)

    avg_clr = [0, 0, 0]
    for (percent, color) in palitra:
        avg_clr += color * percent
    average_color_HEX = "#{:02x}{:02x}{:02x}".format(int(avg_clr[0]), int(avg_clr[1]), int(avg_clr[2]))

    palitra_HEX = []
    for (percent, color) in palitra:
        palitra_HEX.append("#{:02x}{:02x}{:02x} ".format(int(color[0]), int(color[1]), int(color[2])) + "{:0.2f}%".format(percent * 100))

    context = {
        'image': image,
        'dominant_color': dominant_color_HEX,
        'average_color': average_color_HEX,
        'palette': palitra_HEX,
        'admin': admin,
    }
    return render(request, 'images/image_details.html', context)

def image_new(request):
    if request.method == "POST" and request.FILES:
        form = ImageForm(request.POST)
        if form.is_valid():
            image = form.save(commit=False)
            image.author = request.user

            file = request.FILES['content']
            #dir = settings.MEDIA_ROOT+'/img/'
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            #file_url = fs.url(filename)
            image.content = file.name
            image.save()
            return redirect('image_details', pk=image.pk)
    else:
        form = ImageForm()
    return render(request, 'images/image_edit.html', {'form': form})

def image_edit(request, pk):
    image = get_object_or_404(Image, pk=pk)
    file_name_old = image.content.url[1::]
    if request.method == "POST" and request.FILES:
        form = ImageForm(request.POST, instance=image)
        if form.is_valid():
            image = form.save(commit=False)
            image.author = request.user
            image.last_modified = timezone.now()

            fs = FileSystemStorage()
            fs.delete(file_name_old)

            file_new = request.FILES['content']
            #dir = settings.MEDIA_ROOT+'/img/'
            #fs = FileSystemStorage()
            filename = fs.save(file_new.name, file_new)
            # file_url = fs.url(filename)
            image.content = file_new.name

            image.save()
            return redirect('image_details', pk=image.pk)
    else:
        form = ImageForm(instance=image)
    return render(request, 'images/image_edit.html', {'form': form})

def image_delete(request, pk):
    image = get_object_or_404(Image, pk=pk)
    file_name_old = image.content.url[1::]
    fs = FileSystemStorage()
    fs.delete(file_name_old)
    image.delete()
    return redirect('image_list')

class SearchResults(ListView):
    paginate_by = 35
    model = Image
    template_name = 'images/search_results.html'


    def get_queryset(self):  # новый
        query = self.request.GET.get('q')
        object_list = Image.objects.filter(description__icontains=query).order_by('-created_date')
        return object_list
