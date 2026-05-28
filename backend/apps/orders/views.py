import uuid
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.users.decorators import verify_bearer_token
from apps.cart.models import CartItem
from .models import Order, OrderItem

def _ok(data=None, message='Success', status_code=status.HTTP_200_OK):
    return Response({'status': True, 'message': message, 'data': data if data is not None else {}}, status=status_code)

def _fail(message, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({'status': False, 'message': message}, status=status_code)

@api_view(['POST'])
@verify_bearer_token
def checkout(request):
    user = request.user
    customer = request.data.get('customer', {})
    payment_method = request.data.get('payment_method', 'upi')
    if not customer.get('name') or not customer.get('email') or not customer.get('phone'):
        return _fail('Customer name, email and phone are required')

    cart_items = list(CartItem.objects.filter(user=user).select_related('voucher'))
    if not cart_items:
        return _fail('Cart is empty')

    subtotal = sum(i.voucher.price * i.qty for i in cart_items)
    savings = sum((i.voucher.original_price - i.voucher.price) * i.qty for i in cart_items)
    order = Order.objects.create(
        order_id=f'VH-{uuid.uuid4().hex[:10].upper()}',
        user=user,
        customer_name=customer['name'],
        customer_email=customer['email'],
        customer_phone=customer['phone'],
        payment_method=payment_method,
        subtotal=subtotal,
        savings=savings,
        total=subtotal,
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            voucher=item.voucher,
            qty=item.qty,
            unit_price=item.voucher.price,
            unit_original_price=item.voucher.original_price,
            voucher_code=f'VC-{uuid.uuid4().hex[:12].upper()}',
        )
    CartItem.objects.filter(user=user).delete()

    return _ok({'order_id': order.order_id, 'total': order.total}, 'Order placed', status.HTTP_201_CREATED)

@api_view(['GET'])
@verify_bearer_token
def order_detail(request, order_id):
    try:
        order = Order.objects.prefetch_related('items__voucher').get(order_id=order_id, user=request.user)
    except Order.DoesNotExist:
        return _fail('Order not found', status.HTTP_404_NOT_FOUND)

    payload = {
        'order_id': order.order_id,
        'customer_name': order.customer_name,
        'customer_email': order.customer_email,
        'customer_phone': order.customer_phone,
        'payment_method': order.payment_method,
        'subtotal': order.subtotal,
        'savings': order.savings,
        'total': order.total,
        'status': order.status,
        'items': [
            {
                'voucher': item.voucher.name,
                'qty': item.qty,
                'unit_price': item.unit_price,
                'voucher_code': item.voucher_code,
            }
            for item in order.items.all()
        ],
        'created_at': order.created_at,
    }
    return _ok(payload, 'Order fetched')

@api_view(['GET'])
@verify_bearer_token
def order_by_user(request):
    print(f"\n[DEBUG] Fetching orders for user ID: {request.user.id} (Email: {request.user.email})\n")
    orders = Order.objects.filter(user=request.user).prefetch_related('items', 'items__voucher').order_by('-created_at')
    print(f"[DEBUG] Found {orders.count()} orders.")
    data = []
    for o in orders:
        items = [
            {
                'voucher': i.voucher.name,
                'qty': i.qty,
                'unit_price': i.unit_price,
                'voucher_code': i.voucher_code if o.status in ['paid', 'completed'] else 'Available after payment',
            }
            for i in o.items.all()
        ]
        data.append({
            'order_id': o.order_id,
            'total': o.total,
            'status': o.status,
            'created_at': o.created_at,
            'items': items,
        })
    return _ok(data, 'Orders fetched')
