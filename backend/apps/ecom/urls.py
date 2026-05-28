from django.urls import path
from . import views

urlpatterns = [
    # Products (Renamed from Vouchers)
    path('products/', views.product_list, name='product-list'),
    path('vouchers/', views.product_list, name='voucher-list-alias'),
    path('products/<str:product_id>/', views.product_detail, name='product-detail'),
    path('vouchers/<str:product_id>/', views.product_detail, name='voucher-detail-alias'),
    
    # Cart
    path('cart/', views.cart_get, name='cart-get'),
    path('cart/items/', views.cart_add_item, name='cart-add'),
    path('cart/items/<str:product_id>/', views.cart_update_item, name='cart-update'),
    path('cart/remove/<str:product_id>/', views.cart_remove_item, name='cart-remove'),

    
    # Orders
    path('orders/', views.order_by_user, name='order-list'),
    path('orders/checkout/', views.checkout, name='checkout'),
    
    # Content
    path('content/faq/', views.faq_list, name='faq-list'),
    path('content/testimonials/', views.testimonial_list, name='testimonial-list'),
    path('content/contact/', views.contact_create, name='contact-create'),
]
