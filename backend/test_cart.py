import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.users.models import UserProfile
from apps.store.models import Voucher
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

user = UserProfile.objects.first()
token, _ = Token.objects.get_or_create(user=user)

client = APIClient()
client.credentials(HTTP_AUTHORIZATION='Bearer ' + token.key)

voucher = Voucher.objects.first()
print(f"Testing voucher: {voucher.slug_id}")

response = client.post('/api/v1/cart/items/', {'voucher_id': voucher.slug_id, 'qty': 1}, format='json')
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
