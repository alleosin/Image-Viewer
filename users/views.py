from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.core.paginator import Paginator

from images.models import Image
from users.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

# Create your views here.
from users.models import User


class Register(View):

    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data.get('username')
            new_user.set_password(form.cleaned_data.get('password1'))
            new_user.save()
            new_user.groups.add(Group.objects.get(name='User'))
            login_user = authenticate(request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
            if login_user:
                login(request, login_user)
                return redirect('image_list')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

'''def password_change2(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('new_password1'))
            user.save()
            return redirect('home')
        else:
            context = {
                'form': form
            }
            return render(request, 'registration/password_change2.html', context)
    else:
        context = {
            'form': PasswordChangeForm(user=request.user)
        }
        return render(request, 'registration/password_change2.html', context)'''

def user_page(request, username):
    owner = get_object_or_404(User, username=username)
    images = Image.objects.filter(author=owner).order_by('-created_date')

    paginator = Paginator(images, 35)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user_admin = False
    if request.user.groups.filter(name="Admin").exists():
        user_admin = True

    owner_admin = False
    if owner.groups.filter(name="Admin").exists():
        owner_admin = True

    context = {
        'page_obj': page_obj,
        'owner': owner,
        'owner_admin': owner_admin,
        'user_admin': user_admin,
    }
    return render(request, 'users/user_page.html', context)

def user_delete(request, username):
    user = get_object_or_404(User, username=username)
    user.delete()
    return redirect('image_list')

def user_add_to_admin(request, username):
    user = get_object_or_404(User, username=username)
    user.groups.add(Group.objects.get(name='Admin'))
    user.save()
    return redirect('user_page', username)

class UserNew(Register):
    template_name = 'registration/user_new.html'

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data.get('username')
            new_user.set_password(form.cleaned_data.get('password1'))
            new_user.save()
            new_user.groups.add(Group.objects.get(name='User'))
            return redirect('user_page', new_user.username)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
