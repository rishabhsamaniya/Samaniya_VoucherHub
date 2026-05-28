from rest_framework import serializers
from .models import (
    Tag, Category, Product, ProductImage, 
    Cart, CartItem, Order, OrderItem,
    FAQ, Testimonial, ContactMessage
)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductSerializer(serializers.ModelSerializer):
    discount_percent = serializers.ReadOnlyField()
    category = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'slug_id', 'name', 'brand', 'category', 'tags', 'icon', 
            'icon_image', 'image', 'price', 'original_price', 'discount_percent', 'stock'
        ]

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_brand = serializers.ReadOnlyField(source='product.brand')
    product_icon = serializers.ReadOnlyField(source='product.icon')
    product_price = serializers.ReadOnlyField(source='product.price')
    product_original_price = serializers.ReadOnlyField(source='product.original_price')
    product_slug = serializers.ReadOnlyField(source='product.slug_id')
    line_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product_slug', 'product_name', 'product_brand', 'product_icon', 'product_price', 'product_original_price', 'qty', 'line_total']

    def get_line_total(self, obj):
        return obj.product.price * obj.qty

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'customer_name', 'city', 'rating', 'review']
