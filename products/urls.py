from django.urls import path
from .views import *


urlpatterns = [
    path(r'', index, name='product_index'),
    path('create/', add, name='create_product'),
    path('edit/<int:product_id>/', edit, name='edit_product'),
]
