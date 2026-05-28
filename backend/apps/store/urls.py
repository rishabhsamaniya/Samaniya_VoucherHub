from django.urls import path
from . import views

urlpatterns = [
    path('vouchers/', views.vouchers_list, name='v1-vouchers-list'),
    path('vouchers/<str:voucher_id>/', views.voucher_detail, name='v1-voucher-detail'),
    path('content/faq/', views.faq_list, name='v1-faq'),
    path('content/testimonials/', views.testimonial_list, name='v1-testimonials'),
    path('content/contact/', views.contact_create, name='v1-contact-create'),
]
