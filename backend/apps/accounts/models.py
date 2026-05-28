from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Country(TimeStampedModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    def __str__(self): return self.name
    class Meta: verbose_name_plural = "Countries"

class Zone(TimeStampedModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='zones')
    name = models.CharField(max_length=100)
    def __str__(self): return f"{self.name} ({self.country.code})"

class State(TimeStampedModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states')
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True, blank=True, related_name='states')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, blank=True)
    def __str__(self): return f"{self.name}, {self.country.code}"


class City(TimeStampedModel):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=100)
    def __str__(self): return self.name
    class Meta: verbose_name_plural = "Cities"

class Pincode(TimeStampedModel):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='pincodes')
    code = models.CharField(max_length=10, unique=True)
    def __str__(self): return f"{self.code} ({self.city.name})"


class UserProfileManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone: raise ValueError('The Phone Number must be set')
        user = self.model(phone=phone, **extra_fields)
        if password: user.set_password(password)
        else: user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, password, **extra_fields)

class UserProfile(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    phone = models.CharField(max_length=16, unique=True)
    full_name = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True, unique=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    def __str__(self): return self.email or self.phone

class Address(TimeStampedModel):
    ADDRESS_TYPES = (
        ('home', 'Home'),
        ('office', 'Office'),
        ('other', 'Other'),
    )

    # Ownership & Tracking
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='addresses')
    created_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='addresses_created')
    updated_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='addresses_updated')
    
    # Core Details
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPES, default='home')
    full_name = models.CharField(max_length=120)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=16)
    
    street_address = models.TextField()
    landmark = models.CharField(max_length=255, blank=True)
    locality = models.CharField(max_length=255, blank=True)
    
    # Location Hierarchy
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='addresses')
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True, blank=True, related_name='addresses')
    state = models.ForeignKey(State, on_delete=models.PROTECT, related_name='addresses')
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='addresses')
    pincode = models.ForeignKey(Pincode, on_delete=models.PROTECT, related_name='addresses', null=True, blank=True)
    
    company = models.CharField(max_length=255, blank=True)

    
    # Flags
    is_default = models.BooleanField(default=False)
    is_otp_verified = models.BooleanField(default=False)
    
    # Raw fallbacks
    raw_state = models.CharField(max_length=100, blank=True)
    raw_city = models.CharField(max_length=100, blank=True)
    raw_pincode = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.street_address[:30]}, {self.raw_city or self.city.name}"
    
    class Meta:
        verbose_name_plural = "Addresses"

