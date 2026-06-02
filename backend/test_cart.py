import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.accounts.models import UserProfile
from apps.ecom.models import Product
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

user = UserProfile.objects.first()
token, _ = Token.objects.get_or_create(user=user)

client = APIClient()
client.credentials(HTTP_AUTHORIZATION='Bearer ' + token.key)

product = Product.objects.first()
if product:
    print(f"Testing product: {product.slug_id}")
    response = client.post('/api/v1/cart/items/', {'product_id': product.slug_id, 'qty': 1}, format='json')
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
else:
    print("No products found in DB to test.")

