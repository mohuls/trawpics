from turtle import home
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('stock/', stock, name='stock'),
    path('item/<int:id>/', item, name='item'),
    path('pricing/', pricing, name='pricing'),
    path('testimonials/', testimonials, name='testimonials'),


    path('admin-area/', admin_area, name='admin_area'),
    path('admin-area/stock/', admin_stock, name='admin_stock'),
    path('admin-area/orders/', admin_order, name='admin_order'),
]