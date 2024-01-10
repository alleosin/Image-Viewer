from django.urls import path, include
from . import views

urlpatterns = [
    #path('home/', views.home, name='home'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.Register.as_view(), name='register'),
    #path('password_change2/', views.password_change2, name='password_change2'),
    path('new/', views.UserNew.as_view(), name='user_new'),
    path('<str:username>/', views.user_page, name='user_page'),
    path('<str:username>/delete/', views.user_delete, name='user_delete'),
    path('<str:username>/add_to_admin/', views.user_add_to_admin, name='user_add_to_admin'),
]