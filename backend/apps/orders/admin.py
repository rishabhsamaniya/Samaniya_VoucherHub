from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'customer_name', 'total', 'status', 'created_at')
    search_fields = ('order_id', 'customer_name', 'customer_email', 'customer_phone')
    list_filter = ('status', 'payment_method')
    inlines = [OrderItemInline]
