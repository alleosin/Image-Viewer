from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.image_list, name='image_list'),
    path('image/<int:pk>/', views.image_details, name='image_details'),
    path('image/new/', views.image_new, name='image_new'),
    path('image/<int:pk>/edit/', views.image_edit, name='image_edit'),
    path('image/<int:pk>/delete/', views.image_delete, name='image_delete'),
    path('search/', views.SearchResults.as_view(), name='search_results'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
