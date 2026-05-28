from django.db import models
from apps.users.models import UserProfile
from apps.store.models import Voucher

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Order(TimeStampedModel):
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    order_id = models.CharField(max_length=40, unique=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='orders')
    customer_name = models.CharField(max_length=120)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=16)
    payment_method = models.CharField(max_length=30, default='upi')
    subtotal = models.PositiveIntegerField(default=0)
    savings = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='paid')

    def __str__(self):
        return self.order_id

class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    voucher = models.ForeignKey(Voucher, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField(default=1)
    unit_price = models.PositiveIntegerField(default=0)
    unit_original_price = models.PositiveIntegerField(default=0)
    voucher_code = models.CharField(max_length=40)
