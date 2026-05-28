from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Voucher, FAQ, Testimonial, ContactMessage
from .serializers import VoucherSerializer, FAQSerializer, TestimonialSerializer

def _ok(data=None, message='Success', status_code=status.HTTP_200_OK):
    return Response({'status': True, 'message': message, 'data': data if data is not None else {}}, status=status_code)

def _fail(message, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({'status': False, 'message': message}, status=status_code)

@api_view(['GET'])
def vouchers_list(request):
    category = request.query_params.get('category')
    search = request.query_params.get('search')
    qs = Voucher.objects.filter(is_active=True)
    if category and category != 'all':
        qs = qs.filter(category=category)
    if search:
        qs = qs.filter(Q(name__icontains=search) | Q(brand__icontains=search) | Q(category__icontains=search))
    return _ok(VoucherSerializer(qs.order_by('name'), many=True).data, 'Vouchers fetched')

@api_view(['GET'])
def voucher_detail(request, voucher_id):
    try:
        voucher = Voucher.objects.get(slug_id=voucher_id, is_active=True)
    except Voucher.DoesNotExist:
        return _fail('Voucher not found', status.HTTP_404_NOT_FOUND)
    return _ok(VoucherSerializer(voucher).data, 'Voucher fetched')

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
    name = request.data.get('name')
    email = request.data.get('email')
    message = request.data.get('message')
    phone = request.data.get('phone', '')
    if not name or not email or not message:
        return _fail('name, email and message are required')
    contact = ContactMessage.objects.create(name=name, email=email, phone=phone, message=message)
    return _ok({'id': contact.id}, 'Contact request submitted', status.HTTP_201_CREATED)
