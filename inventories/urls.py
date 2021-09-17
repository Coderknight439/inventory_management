from django.urls import path
from .views import *


urlpatterns = [
    path(r'', index, name='inventory_index'),
    path('create/', add, name='create_inventory'),
    path('edit/<int:inventory_id>/', edit, name='edit_inventory'),
    path('delete/<int:inventory_id>/', delete, name='delete_inventory'),

]
