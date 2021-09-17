from django.urls import path
from .views import *


urlpatterns = [
    path(r'', index, name='order_index'),
    path('create/', add, name='create_order'),
    path('pending/<int:order_id>/', pending, name='pending_order'),
    path('complete/<int:order_id>/', complete, name='complete_order'),
    path('reject/<int:order_id>/', reject, name='reject_order'),
    path('view/<int:order_id>/', view, name='view_order'),

]
