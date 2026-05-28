from django.db import models
from apps.accounts.models import UserProfile

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Tag(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Tagss"  # As requested in the image

class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categorys"  # As requested in the image

class Product(TimeStampedModel):
    slug_id = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=160)
    brand = models.CharField(max_length=120)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    tags = models.ManyToManyField(Tag, blank=True, related_name='products')
    icon = models.CharField(max_length=8, default='🎫', help_text="Emoji fallback")
    icon_image = models.ImageField(upload_to='icons/', null=True, blank=True)
    image = models.ImageField(upload_to='vouchers/', null=True, blank=True)
    price = models.PositiveIntegerField()
    original_price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=100)
    is_active = models.BooleanField(default=True)

    @property
    def discount_percent(self):
        if self.original_price <= 0: return 0
        return round((self.original_price - self.price) * 100 / self.original_price)

    def __str__(self):
        return f'{self.name} ({self.slug_id})'

    class Meta:
        verbose_name_plural = "Products"

class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"

    class Meta:
        verbose_name_plural = "Product images"

class Cart(TimeStampedModel):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='cart')
    
    def __str__(self):
        return f"Cart of {self.user.email}"

    class Meta:
        verbose_name_plural = "Carts"

class CartItem(TimeStampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.qty} x {self.product.name}"

    class Meta:
        verbose_name_plural = "Cart items"
        unique_together = ('cart', 'product')

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

    class Meta:
        verbose_name_plural = "Orders"

class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField(default=1)
    unit_price = models.PositiveIntegerField(default=0)
    unit_original_price = models.PositiveIntegerField(default=0)
    voucher_code = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.order.order_id} - {self.product.name}"

    class Meta:
        verbose_name_plural = "Order items"

class FAQ(TimeStampedModel):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self): return self.question

class Testimonial(TimeStampedModel):
    customer_name = models.CharField(max_length=120)
    city = models.CharField(max_length=80, blank=True)
    rating = models.PositiveSmallIntegerField(default=5)
    review = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self): return self.customer_name

class ContactMessage(TimeStampedModel):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=16, blank=True)
    message = models.TextField()

    def __str__(self): return self.name

