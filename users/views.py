from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group

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
    user = get_object_or_404(User, username=username)
    images = Image.objects.filter(author=user).order_by('-created_date')
    context = {
        'images': images,
        'username': username,
    }
    return render(request, 'users/user_page.html', context)
