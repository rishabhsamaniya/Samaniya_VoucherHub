from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.email_signup, name='signup'),
    path('login/', views.email_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/request/', views.password_reset_request, name='password-reset-request'),
    path('password-reset/confirm/', views.password_reset_confirm, name='password-reset-confirm'),
    
    # Addresses
    path('addresses/', views.address_list_create, name='address-list-create'),
    path('addresses/default/', views.get_default_address, name='address-default'),
    path('states/search/', views.state_search, name='state-search'),
    path('pincodes/lookup/', views.pincode_lookup, name='pincode-lookup'),
]


