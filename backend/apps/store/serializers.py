from rest_framework import serializers
from .models import Voucher, FAQ, Testimonial, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class VoucherSerializer(serializers.ModelSerializer):
    discount_percent = serializers.ReadOnlyField()
    category = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = Voucher
        fields = [
            'id', 'slug_id', 'name', 'brand', 'category', 'icon', 'icon_image', 'image',
            'price', 'original_price', 'discount_percent', 'stock'
        ]


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'customer_name', 'city', 'rating', 'review']
