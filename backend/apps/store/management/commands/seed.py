from django.core.management.base import BaseCommand
from apps.store.models import Voucher
import random

class Command(BaseCommand):
    help = 'Seeds the database with 10 dummy vouchers for testing'

    def handle(self, *args, **kwargs):
        vouchers_data = [
            {'category': 'shopping', 'icon': '🛍️', 'slug_id': 'amz-500', 'name': 'Amazon Gift Card ₹500', 'brand': 'Amazon', 'price': 480, 'original_price': 500, 'stock': 200},
            {'category': 'shopping', 'icon': '🛍️', 'slug_id': 'flp-1000', 'name': 'Flipkart Gift Card ₹1000', 'brand': 'Flipkart', 'price': 940, 'original_price': 1000, 'stock': 150},
            {'category': 'gaming', 'icon': '🎮', 'slug_id': 'stm-750', 'name': 'Steam Wallet ₹750', 'brand': 'Steam', 'price': 720, 'original_price': 750, 'stock': 100},
            {'category': 'gaming', 'icon': '🎮', 'slug_id': 'psn-1500', 'name': 'PlayStation Store ₹1500', 'brand': 'Sony', 'price': 1425, 'original_price': 1500, 'stock': 50},
            {'category': 'streaming', 'icon': '🍿', 'slug_id': 'nfx-649', 'name': 'Netflix Premium 1 Month', 'brand': 'Netflix', 'price': 599, 'original_price': 649, 'stock': 300},
            {'category': 'streaming', 'icon': '🍿', 'slug_id': 'spt-119', 'name': 'Spotify Premium 1 Month', 'brand': 'Spotify', 'price': 100, 'original_price': 119, 'stock': 400},
            {'category': 'food', 'icon': '🍔', 'slug_id': 'zmt-200', 'name': 'Zomato Voucher ₹200', 'brand': 'Zomato', 'price': 180, 'original_price': 200, 'stock': 250},
            {'category': 'food', 'icon': '🍔', 'slug_id': 'swg-250', 'name': 'Swiggy Voucher ₹250', 'brand': 'Swiggy', 'price': 225, 'original_price': 250, 'stock': 300},
            {'category': 'travel', 'icon': '✈️', 'slug_id': 'mmy-2000', 'name': 'MakeMyTrip Gift Card ₹2000', 'brand': 'MakeMyTrip', 'price': 1850, 'original_price': 2000, 'stock': 80},
            {'category': 'fashion', 'icon': '👗', 'slug_id': 'mynt-1000', 'name': 'Myntra E-Gift ₹1000', 'brand': 'Myntra', 'price': 900, 'original_price': 1000, 'stock': 120},
        ]
        
        created_count = 0
        for v in vouchers_data:
            obj, created = Voucher.objects.get_or_create(
                slug_id=v['slug_id'],
                defaults=v
            )
            if created:
                created_count += 1
                
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {created_count} dummy vouchers.'))
