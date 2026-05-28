from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.users.decorators import verify_bearer_token
from apps.store.models import Voucher
from .models import CartItem

def _ok(data=None, message='Success', status_code=status.HTTP_200_OK):
    return Response({'status': True, 'message': message, 'data': data if data is not None else {}}, status=status_code)

def _fail(message, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({'status': False, 'message': message}, status=status_code)

def _cart_summary(user):
    items = CartItem.objects.filter(user=user).select_related('voucher')
    payload = []
    subtotal = 0
    savings = 0
    for item in items:
        line_total = item.voucher.price * item.qty
        subtotal += line_total
        savings += (item.voucher.original_price - item.voucher.price) * item.qty
        payload.append(
            {
                'id': item.id,
                'voucher_id': item.voucher.slug_id,
                'name': item.voucher.name,
                'brand': item.voucher.brand,
                'icon': item.voucher.icon,
                'price': item.voucher.price,
                'original_price': item.voucher.original_price,
                'qty': item.qty,
                'line_total': line_total,
            }
        )
    return {
        'items': payload,
        'summary': {'subtotal': subtotal, 'savings': savings, 'total': subtotal},
    }

@api_view(['GET'])
@verify_bearer_token
def cart_get(request):
    user = request.user
    return _ok(_cart_summary(user), 'Cart fetched')

@api_view(['POST'])
@verify_bearer_token
def cart_add_item(request):
    user = request.user

    voucher_id = request.data.get('voucher_id')
    qty = int(request.data.get('qty', 1))
    if qty < 1:
        return _fail('Quantity must be at least 1')
    try:
        voucher = Voucher.objects.get(slug_id=voucher_id, is_active=True)
    except Voucher.DoesNotExist:
        return _fail('Voucher not found', status.HTTP_404_NOT_FOUND)

    item, created = CartItem.objects.get_or_create(user=user, voucher=voucher, defaults={'qty': qty})
    if created:
        if qty > voucher.stock:
            item.delete()
            return _fail('Not enough stock for this voucher', status.HTTP_400_BAD_REQUEST)
        return _ok(_cart_summary(user), 'Item added to cart')

    new_qty = item.qty + qty
    if new_qty > voucher.stock:
        return _fail('Not enough stock for this voucher', status.HTTP_400_BAD_REQUEST)
    item.qty = new_qty
    item.save(update_fields=['qty', 'updated_at'])
    return _ok(_cart_summary(user), 'Item added to cart')

@api_view(['PATCH'])
@verify_bearer_token
def cart_update_item(request, voucher_id):
    qty = int(request.data.get('qty', 1))
    if qty < 1:
        return _fail('Quantity must be at least 1')
    try:
        user = request.user
        voucher = Voucher.objects.get(slug_id=voucher_id)
        item = CartItem.objects.get(user=user, voucher=voucher)
    except (Voucher.DoesNotExist, CartItem.DoesNotExist):
        return _fail('Cart item not found', status.HTTP_404_NOT_FOUND)

    if qty > voucher.stock:
        return _fail('Not enough stock for this voucher', status.HTTP_400_BAD_REQUEST)

    item.qty = qty
    item.save(update_fields=['qty', 'updated_at'])
    return _ok(_cart_summary(user), 'Cart item updated')

@api_view(['DELETE'])
@verify_bearer_token
def cart_remove_item(request, voucher_id):
    try:
        user = request.user
        voucher = Voucher.objects.get(slug_id=voucher_id)
        CartItem.objects.filter(user=user, voucher=voucher).delete()
    except Voucher.DoesNotExist:
        return _fail('Cart item not found', status.HTTP_404_NOT_FOUND)
    return _ok(_cart_summary(user), 'Item removed')

@api_view(['DELETE'])
@verify_bearer_token
def cart_clear(request):
    user = request.user
    CartItem.objects.filter(user=user).delete()
    return _ok(_cart_summary(user), 'Cart cleared')
