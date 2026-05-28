from django.db import models
from apps.users.models import UserProfile
from apps.store.models import Voucher

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CartItem(TimeStampedModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='cart_items')
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'voucher')
