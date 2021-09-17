from django.urls import path
from .views import *


urlpatterns = [
    path(r'', index, name='vendor_index'),
    path('create/', add, name='create_vendor'),
    path('edit/<int:vendor_id>/', edit, name='edit_vendor'),
    path('delete/<int:vendor_id>/', delete, name='delete_vendor'),

]
