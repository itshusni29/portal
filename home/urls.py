
from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('pages/', views.pages, name='pages'),
    path('files/', views.file_list, name='file_list'),
    path('files/upload/', views.upload_file, name='upload_file'),
    path('files/delete/<int:pk>/', views.delete_file, name='delete_file'),
    
    re_path(r'^.*\.*', views.pages, name='pages'),
]
