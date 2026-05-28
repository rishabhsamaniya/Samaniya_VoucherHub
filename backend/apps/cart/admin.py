from django.contrib import admin
from .models import CartItem

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'voucher', 'qty', 'updated_at')
    search_fields = ('user__phone', 'user__email', 'voucher__name')
