import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import UserProfile
from apps.ecom.models import Category, Product, FAQ, Testimonial
from seed_geo import seed_geo

# 1. Seed Geographic Data
print("=== Seeding Geographic Data ===")
try:
    seed_geo()
    print("Geographic data seeded successfully.")
except Exception as e:
    print(f"Error seeding geographic data: {e}")

# 2. Create Superuser
print("=== Checking Superuser ===")
if not UserProfile.objects.filter(is_superuser=True).exists():
    print("Creating default superuser...")
    UserProfile.objects.create_superuser(
        email="admin@example.com",
        phone="9999999999",
        password="adminpassword123",
        full_name="Admin User"
    )
    print("Superuser created: email=admin@example.com, password=adminpassword123")
else:
    print("Superuser already exists.")

# 3. Seed Categories & Products
print("=== Seeding Categories and Vouchers ===")
categories_data = [
    {'name': 'Shopping', 'slug': 'shopping'},
    {'name': 'Gaming', 'slug': 'gaming'},
    {'name': 'Streaming', 'slug': 'streaming'},
    {'name': 'Food', 'slug': 'food'},
    {'name': 'Travel', 'slug': 'travel'},
    {'name': 'Fashion', 'slug': 'fashion'},
]

category_cache = {}
for cat_info in categories_data:
    cat_obj, _ = Category.objects.get_or_create(slug=cat_info['slug'], defaults={'name': cat_info['name']})
    category_cache[cat_info['slug']] = cat_obj

vouchers_data = [
    # Amazon Gift Cards
    {'category': 'shopping', 'icon': '🛍️', 'slug_id': 'amz-100', 'name': 'Amazon Gift Card ₹100', 'brand': 'Amazon', 'price': 96, 'original_price': 100, 'stock': 300, 'image': 'vouchers/amazon_voucher.png'},
    {'category': 'shopping', 'icon': '🛍️', 'slug_id': 'amz-250', 'name': 'Amazon Gift Card ₹250', 'brand': 'Amazon', 'price': 240, 'original_price': 250, 'stock': 250, 'image': 'vouchers/amazon_voucher.png'},
    {'category': 'shopping', 'icon': '🛍️', 'slug_id': 'amz-500', 'name': 'Amazon Gift Card ₹500', 'brand': 'Amazon', 'price': 480, 'original_price': 500, 'stock': 200, 'image': 'vouchers/amazon_voucher.png'},
    {'category': 'shopping', 'icon': '🛍️', 'slug_id': 'amz-1000', 'name': 'Amazon Gift Card ₹1000', 'brand': 'Amazon', 'price': 950, 'original_price': 1000, 'stock': 180, 'image': 'vouchers/amazon_voucher.png'},
    {'category': 'shopping', 'icon': '🛍️', 'slug_id': 'amz-2000', 'name': 'Amazon Gift Card ₹2000', 'brand': 'Amazon', 'price': 1900, 'original_price': 2000, 'stock': 150, 'image': 'vouchers/amazon_voucher.png'},
    {'category': 'shopping', 'icon': '🛍️', 'slug_id': 'amz-5000', 'name': 'Amazon Gift Card ₹5000', 'brand': 'Amazon', 'price': 4700, 'original_price': 5000, 'stock': 100, 'image': 'vouchers/amazon_voucher.png'},
    
    # Flipkart Gift Cards
    {'category': 'shopping', 'icon': '🛍️', 'slug_id': 'flp-100', 'name': 'Flipkart Gift Card ₹100', 'brand': 'Flipkart', 'price': 95, 'original_price': 100, 'stock': 300, 'image': 'vouchers/flipkart_voucher.png'},
    {'category': 'shopping', 'icon': '🛍️', 'slug_id': 'flp-250', 'name': 'Flipkart Gift Card ₹250', 'brand': 'Flipkart', 'price': 238, 'original_price': 250, 'stock': 250, 'image': 'vouchers/flipkart_voucher.png'},
    {'category': 'shopping', 'icon': '🛍️', 'slug_id': 'flp-500', 'name': 'Flipkart Gift Card ₹500', 'brand': 'Flipkart', 'price': 475, 'original_price': 500, 'stock': 200, 'image': 'vouchers/flipkart_voucher.png'},
    {'category': 'shopping', 'icon': '🛍️', 'slug_id': 'flp-1000', 'name': 'Flipkart Gift Card ₹1000', 'brand': 'Flipkart', 'price': 940, 'original_price': 1000, 'stock': 150, 'image': 'vouchers/flipkart_voucher.png'},
    {'category': 'shopping', 'icon': '🛍️', 'slug_id': 'flp-2000', 'name': 'Flipkart Gift Card ₹2000', 'brand': 'Flipkart', 'price': 1880, 'original_price': 2000, 'stock': 120, 'image': 'vouchers/flipkart_voucher.png'},
    {'category': 'shopping', 'icon': '🛍️', 'slug_id': 'flp-5000', 'name': 'Flipkart Gift Card ₹5000', 'brand': 'Flipkart', 'price': 4650, 'original_price': 5000, 'stock': 80, 'image': 'vouchers/flipkart_voucher.png'},
]

for v in vouchers_data:
    cat_obj = category_cache.get(v['category'])
    if cat_obj:
        Product.objects.get_or_create(
            slug_id=v['slug_id'],
            defaults={
                'name': v['name'],
                'brand': v['brand'],
                'category': cat_obj,
                'icon': v['icon'],
                'price': v['price'],
                'original_price': v['original_price'],
                'stock': v['stock'],
                'is_active': True,
                'image': v.get('image')
            }
        )
print("Products and Categories populated successfully.")

# 4. Seed FAQs
print("=== Seeding FAQs ===")
faqs = [
    ("What is Samaniya VoucherHub?", "Samaniya VoucherHub is India's leading platform for buying discounted digital vouchers and gift cards. We partner directly with top brands like Amazon, Flipkart, Netflix, Steam, and hundreds more to offer you genuine vouchers at up to 40% discount."),
    ("Are the voucher codes genuine?", "Absolutely. Every voucher on Samaniya VoucherHub is sourced directly from official brand partners. We guarantee 100% genuine codes."),
    ("Is payment secure on Samaniya VoucherHub?", "Yes. Samaniya VoucherHub uses bank-grade 256-bit SSL encryption for all transactions. We are PCI-DSS compliant and never store your card or banking details.")
]
for q, a in faqs:
    FAQ.objects.get_or_create(question=q, defaults={'answer': a, 'is_active': True})
print("FAQs populated successfully.")

# 5. Seed Testimonials
print("=== Seeding Testimonials ===")
testimonials = [
    ("Rahul Sharma", "Delhi, India", 5, "Got my Amazon voucher code in literally 10 seconds after payment. Used it immediately. The 20% discount was incredible — will definitely be back!"),
    ("Priya Menon", "Bangalore, India", 5, "Best platform for gifting. I bought 5 Flipkart vouchers for my team and the entire process took under 2 minutes. Super smooth experience!"),
    ("Arjun Patel", "Mumbai, India", 5, "The Netflix voucher discount saved me ₹400 on a yearly plan. The site is beautifully designed and payment was extremely secure.")
]
for name, city, rating, review in testimonials:
    Testimonial.objects.get_or_create(customer_name=name, defaults={'city': city, 'rating': rating, 'review': review, 'is_active': True})
print("Testimonials populated successfully.")
print("=== Initialization Script Complete ===")
