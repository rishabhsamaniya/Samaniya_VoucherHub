from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (
    Tag, Category, Product, ProductImage, 
    Cart, CartItem, Order, OrderItem,
    FAQ, Testimonial, ContactMessage
)

@admin.register(Tag)
class TagAdmin(ImportExportModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'stock', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'brand')
    inlines = [ProductImageInline]

@admin.register(ProductImage)
class ProductImageAdmin(ImportExportModelAdmin):
    list_display = ('product', 'image')

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(ImportExportModelAdmin):
    list_display = ('user', 'created_at')
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(ImportExportModelAdmin):
    list_display = ('cart', 'product', 'qty')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    list_display = ('order_id', 'customer_name', 'total', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(ImportExportModelAdmin):
    list_display = ('order', 'product', 'qty', 'unit_price')

@admin.register(FAQ)
class FAQAdmin(ImportExportModelAdmin):
    list_display = ('question', 'is_active')

@admin.register(Testimonial)
class TestimonialAdmin(ImportExportModelAdmin):
    list_display = ('customer_name', 'rating')

@admin.register(ContactMessage)
class ContactAdmin(ImportExportModelAdmin):
    list_display = ('name', 'email', 'created_at')
