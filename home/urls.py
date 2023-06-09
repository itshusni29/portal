from django.urls import path, re_path
from . import views
from .views import edit_product


urlpatterns = [
    path('index', views.index, name='index'),
    path('pages', views.pages, name='pages'),
    path('', views.home, name='home'),
    path('add_product', views.add_product, name='add_product'),
    path('product/<str:product_id>/', views.product, name='product'),
    path('product/<int:product_id>/edit/', edit_product, name='edit_product'),
    path('delete_product/<str:product_id>/', views.delete_product, name='delete_product'),
    re_path(r'^.*\.*', views.pages, name='pages'),
]

