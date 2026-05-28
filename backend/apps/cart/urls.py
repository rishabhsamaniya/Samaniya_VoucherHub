from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_get, name='v1-cart-get'),
    path('items/', views.cart_add_item, name='v1-cart-add-item'),
    path('items/<str:voucher_id>/', views.cart_update_item, name='v1-cart-update-item'),
    path('remove/<str:voucher_id>/', views.cart_remove_item, name='v1-cart-remove-item'),
    path('clear/', views.cart_clear, name='v1-cart-clear'),
]
