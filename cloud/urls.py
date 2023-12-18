from django.urls import path
from .views import *
from .models import Post

from django.views.generic import TemplateView

urlpatterns = [
    path('', index, name='index'),
    path('detail/<int:pk>/', post_detail, name='post_detail'),
    path('download/<int:pk>/', download_file, name='download'),
    path('create/', create_post, name='create_post'),
    path('update/<int:pk>/', update_post, name='update_post'),
    path('delete/<int:pk>/', delete_post, name='delete_post'),


]