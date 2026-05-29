import uuid
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.accounts.decorators import verify_bearer_token
from .models import (
    Tag, Category, Product, ProductImage, 
    Cart, CartItem, Order, OrderItem,
    FAQ, Testimonial, ContactMessage
)
from .serializers import (
    ProductSerializer, FAQSerializer, 
    TestimonialSerializer, CartItemSerializer
)

def _ok(data=None, message='Success', status_code=status.HTTP_200_OK):
    return Response({'status': True, 'message': message, 'data': data if data is not None else {}}, status=status_code)

def _fail(message, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({'status': False, 'message': message}, status=status_code)

def _get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart

def _cart_summary(user):
    cart = _get_or_create_cart(user)
    items = cart.items.select_related('product')
    payload = []
    subtotal = 0      # This will be the original (MRP) subtotal
    total = 0         # This will be the discounted total
    savings = 0
    for item in items:
        line_total = item.product.price * item.qty
        total += line_total
        subtotal += item.product.original_price * item.qty
        savings += (item.product.original_price - item.product.price) * item.qty
        payload.append({
            'id': item.id,
            'product_slug': item.product.slug_id,
            'voucher_id': item.product.slug_id, # Alias for frontend compatibility
            'name': item.product.name,
            'brand': item.product.brand,
            'icon': item.product.icon,
            'price': item.product.price,
            'original_price': item.product.original_price,
            'qty': item.qty,
            'line_total': line_total,
        })
    return {
        'items': payload,
        'summary': {'subtotal': subtotal, 'savings': savings, 'total': total},
    }

# --- Products ---
@api_view(['GET'])
def product_list(request):
    category_slug = request.query_params.get('category')
    search = request.query_params.get('search')
    # Use select_related for category and prefetch_related for tags/images to avoid N+1 queries
    qs = Product.objects.filter(is_active=True).select_related('category').prefetch_related('tags', 'images')
    if category_slug and category_slug != 'all':
        qs = qs.filter(category__slug=category_slug)
    if search:
        qs = qs.filter(Q(name__icontains=search) | Q(brand__icontains=search) | Q(category__name__icontains=search))
    return _ok(ProductSerializer(qs.order_by('name'), many=True).data, 'Products fetched')


@api_view(['GET'])
def product_detail(request, product_id):
    try:
        product = Product.objects.get(slug_id=product_id, is_active=True)
    except Product.DoesNotExist:
        return _fail('Product not found', status.HTTP_404_NOT_FOUND)
    return _ok(ProductSerializer(product).data, 'Product fetched')

# --- Cart ---
@api_view(['GET'])
@verify_bearer_token
def cart_get(request):
    return _ok(_cart_summary(request.user), 'Cart fetched')

@api_view(['POST'])
@verify_bearer_token
def cart_add_item(request):
    user = request.user
    cart = _get_or_create_cart(user)
    product_slug = request.data.get('product_id') or request.data.get('voucher_id')
    qty = int(request.data.get('qty', 1))
    
    try:
        product = Product.objects.get(slug_id=product_slug, is_active=True)
    except Product.DoesNotExist:
        return _fail('Product not found', status.HTTP_404_NOT_FOUND)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'qty': qty})
    if not created:
        item.qty += qty
        item.save()
    
    return _ok(_cart_summary(user), 'Item added to cart')

@api_view(['PATCH'])
@verify_bearer_token
def cart_update_item(request, product_id):
    user = request.user
    cart = _get_or_create_cart(user)
    qty = int(request.data.get('qty', 1))
    
    try:
        item = CartItem.objects.get(cart=cart, product__slug_id=product_id)
        item.qty = qty
        item.save()
    except CartItem.DoesNotExist:
        return _fail('Item not in cart')
        
    return _ok(_cart_summary(user), 'Cart updated')

@api_view(['DELETE'])
@verify_bearer_token
def cart_remove_item(request, product_id):
    user = request.user
    cart = _get_or_create_cart(user)
    CartItem.objects.filter(cart=cart, product__slug_id=product_id).delete()
    return _ok(_cart_summary(user), 'Item removed from cart')


# --- Orders ---
@api_view(['POST'])
@verify_bearer_token
def checkout(request):
    user = request.user
    cart = _get_or_create_cart(user)
    customer = request.data.get('customer', {})
    payment_method = request.data.get('payment_method', 'upi')
    
    cart_items = list(cart.items.select_related('product'))
    if not cart_items:
        return _fail('Cart is empty')

    subtotal = sum(i.product.original_price * i.qty for i in cart_items)
    total = sum(i.product.price * i.qty for i in cart_items)
    savings = sum((i.product.original_price - i.product.price) * i.qty for i in cart_items)
    
    order = Order.objects.create(
        order_id=f'VH-{uuid.uuid4().hex[:10].upper()}',
        user=user,
        customer_name=customer.get('name', ''),
        customer_email=customer.get('email', ''),
        customer_phone=customer.get('phone', ''),
        payment_method=payment_method,
        subtotal=subtotal,
        savings=savings,
        total=total,
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            qty=item.qty,
            unit_price=item.product.price,
            unit_original_price=item.product.original_price,
            voucher_code=f'VC-{uuid.uuid4().hex[:12].upper()}',
        )
    
    cart.items.all().delete()
    return _ok({'order_id': order.order_id, 'total': order.total}, 'Order placed', status.HTTP_201_CREATED)

@api_view(['GET'])
@verify_bearer_token
def order_by_user(request):
    # Optimized fetching with related data
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product', 'items__product__category').order_by('-created_at')

    data = []
    for o in orders:
        data.append({
            'order_id': o.order_id,
            'total': o.total,
            'status': o.status,
            'created_at': o.created_at,
            'items': [
                {
                    'voucher': i.product.name,
                    'qty': i.qty,
                    'unit_price': i.unit_price,
                    'voucher_code': i.voucher_code if o.status in ['paid', 'completed'] else 'Available after payment',
                }
                for i in o.items.all()
            ]
        })
    return _ok(data, 'Orders fetched')

# --- Content ---
@api_view(['GET'])
def faq_list(request):
    qs = FAQ.objects.filter(is_active=True).order_by('id')
    return _ok(FAQSerializer(qs, many=True).data, 'FAQ fetched')

@api_view(['GET'])
def testimonial_list(request):
    qs = Testimonial.objects.filter(is_active=True).order_by('id')
    return _ok(TestimonialSerializer(qs, many=True).data, 'Testimonials fetched')

@api_view(['POST'])
def contact_create(request):
    contact = ContactMessage.objects.create(
        name=request.data.get('name'),
        email=request.data.get('email'),
        phone=request.data.get('phone', ''),
        message=request.data.get('message')
    )
    return _ok({'id': contact.id}, 'Message sent', status.HTTP_201_CREATED)
