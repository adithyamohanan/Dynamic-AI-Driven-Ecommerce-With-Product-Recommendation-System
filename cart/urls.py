# HelloWorldProject/HelloWorldApp/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('cart/',views.view_cart, name = 'view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:order_id>/', views.remove_from_cart, name="remove_from_cart"),
    path('increment/<int:product_id>/', views.increment_cart_item, name='increment_cart_item'),
    path('decrement/<int:product_id>/', views.decrement_cart_item, name='decrement_cart_item'),
    
    
]