import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import UserProfile
from apps.accounts.serializers import AddressSerializer

user = UserProfile.objects.first()
print("User:", user)

data = {
    'full_name': 'Test User',
    'phone': '1234567890',
    'street_address': 'Test Street',
    'raw_city': 'New City XYZ',
    'raw_state': 'New State XYZ',
    'city_name': 'New City XYZ',
    'state_name': 'New State XYZ',
    'zone_name': 'South',
    'pincode_code': '999999'
}

# Create a mock request object
class MockRequest:
    def __init__(self, user, data):
        self.user = user
        self.data = data

serializer = AddressSerializer(data=data, context={'request': MockRequest(user, data)})
if serializer.is_valid():
    print("VALID", serializer.validated_data)
    addr = serializer.save()
    print("Address created:", addr.id)
else:
    print("INVALID", serializer.errors)
