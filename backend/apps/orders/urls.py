from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='v1-checkout'),
    path('', views.order_by_user, name='v1-orders-by-user'),
    path('<str:order_id>/', views.order_detail, name='v1-order-detail'),
]
