from django.shortcuts import render, get_object_or_404
from .models import Image
from sklearn.cluster import KMeans
import cv2
import numpy as np


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
    images = Image.objects.all()
    context = {
        'images': images,
    }
    return render(request, 'images/image_list.html', context)

def image_details(request, pk):
    image = get_object_or_404(Image, pk=pk)

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
    }
    return render(request, 'images/image_details.html', context)
