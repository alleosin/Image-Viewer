from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm

from users.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import View

# Create your views here.

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
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
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
