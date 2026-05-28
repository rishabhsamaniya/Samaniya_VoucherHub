from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Voucher(TimeStampedModel):
    slug_id = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=160)
    brand = models.CharField(max_length=120)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='vouchers')
    icon = models.CharField(max_length=8, default='🎫', help_text="Emoji fallback")
    icon_image = models.ImageField(upload_to='icons/', null=True, blank=True)
    image = models.ImageField(upload_to='vouchers/', null=True, blank=True)
    price = models.PositiveIntegerField()
    original_price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=100)
    is_active = models.BooleanField(default=True)

    @property
    def discount_percent(self):
        if self.original_price <= 0:
            return 0
        return round((self.original_price - self.price) * 100 / self.original_price)

    def __str__(self):
        return f'{self.name} ({self.slug_id})'


class FAQ(TimeStampedModel):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)


class Testimonial(TimeStampedModel):
    customer_name = models.CharField(max_length=120)
    city = models.CharField(max_length=80, blank=True)
    rating = models.PositiveSmallIntegerField(default=5)
    review = models.TextField()
    is_active = models.BooleanField(default=True)


class ContactMessage(TimeStampedModel):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=16, blank=True)
    message = models.TextField()
