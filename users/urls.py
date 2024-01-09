from django.urls import path, include
from . import views

urlpatterns = [
    #path('home/', views.home, name='home'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.Register.as_view(), name='register'),
    #path('password_change2/', views.password_change2, name='password_change2')
]