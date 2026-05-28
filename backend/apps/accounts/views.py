from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .decorators import verify_bearer_token
from .models import UserProfile, Address, Country, State, City, Pincode
from .serializers import UserProfileSerializer, AddressSerializer, StateSerializer

def _ok(data=None, message='Success', status_code=status.HTTP_200_OK):
    return Response({'status': True, 'message': message, 'data': data if data is not None else {}}, status=status_code)

def _fail(message, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({'status': False, 'message': message}, status=status_code)

@api_view(['POST'])
@permission_classes([AllowAny])
def email_signup(request):
    full_name = request.data.get('full_name', '').strip()
    email = request.data.get('email', '').strip()
    phone = request.data.get('phone', '').strip()
    password = request.data.get('password')
    
    if not email or not phone or not password:
        return _fail('Email, phone and password are required.')
        
    if UserProfile.objects.filter(email=email).exists():
        return _fail('Email is already registered.', status_code=status.HTTP_409_CONFLICT)
    if UserProfile.objects.filter(phone=phone).exists():
        return _fail('Phone number is already registered.', status_code=status.HTTP_409_CONFLICT)
        
    user = UserProfile.objects.create_user(phone=phone, password=password, email=email, full_name=full_name)
    token, _ = Token.objects.get_or_create(user=user)
    return _ok({'token': token.key, 'user': UserProfileSerializer(user).data}, 'Account created successfully', status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def email_login(request):
    email = request.data.get('email', '').strip()
    password = request.data.get('password')
    
    if not email or not password:
        return _fail('Email and password are required.')
        
    try:
        user = UserProfile.objects.get(email=email)
        if not user.check_password(password):
            return _fail('Invalid email or password', status_code=status.HTTP_401_UNAUTHORIZED)
    except UserProfile.DoesNotExist:
        return _fail('Invalid email or password', status_code=status.HTTP_401_UNAUTHORIZED)
        
    token, _ = Token.objects.get_or_create(user=user)
    return _ok({'token': token.key, 'user': UserProfileSerializer(user).data}, 'Login successful')

@api_view(['POST'])
@verify_bearer_token
def logout_view(request):
    try:
        request.user.auth_token.delete()
    except:
        pass
    return _ok(message='Logged out successfully')

# --- Password Reset ---
@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    phone = request.data.get('phone', '').strip()
    if not phone: return _fail('Phone number is required')
    try:
        user = UserProfile.objects.get(phone=phone)
        otp = "123456" 
        print(f"\n[AUTH] Password Reset OTP for {phone}: {otp}\n")
        return _ok({'phone': phone}, f'OTP sent to {phone}. Check terminal.')
    except UserProfile.DoesNotExist:
        return _fail('Phone number not found.')

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    phone = request.data.get('phone', '').strip()
    otp = request.data.get('otp', '').strip()
    new_password = request.data.get('new_password', '').strip()
    if otp != "123456": return _fail('Invalid OTP')
    try:
        user = UserProfile.objects.get(phone=phone)
        user.set_password(new_password)
        user.save()
        return _ok(message='Password reset successful.')
    except UserProfile.DoesNotExist:
        return _fail('User not found.')

# --- Addresses ---
@api_view(['GET', 'POST'])
@verify_bearer_token
def address_list_create(request):
    if request.method == 'GET':
        addresses = Address.objects.filter(user=request.user).order_by('-is_default', '-created_at')
        return _ok(AddressSerializer(addresses, many=True).data)
    
    serializer = AddressSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        if request.data.get('is_default'):
            Address.objects.filter(user=request.user).update(is_default=False)
        serializer.save()
        return _ok(serializer.data, 'Address saved successfully', status.HTTP_201_CREATED)
    return _fail(serializer.errors)

@api_view(['GET'])
@verify_bearer_token
def get_default_address(request):
    address = Address.objects.filter(user=request.user, is_default=True).first()
    if not address:
        address = Address.objects.filter(user=request.user).order_by('-created_at').first()
    if address:
        return _ok(AddressSerializer(address).data)
    return _ok(None, 'No address found')

@api_view(['GET'])
@permission_classes([AllowAny])
def state_search(request):

    query = request.query_params.get('q', '')
    if len(query) < 1:
        states = State.objects.filter(country__code='IN').order_by('name')[:10]
    else:
        states = State.objects.filter(country__code='IN', name__icontains=query).order_by('name')
    return _ok(StateSerializer(states, many=True).data)

@api_view(['GET'])
@permission_classes([AllowAny])
def pincode_lookup(request):
    code = request.query_params.get('code', '').strip()
    if not code:
        return _fail("Pincode is required")
        
    pincode = Pincode.objects.filter(code=code).select_related('city', 'city__state', 'city__state__country', 'city__state__zone').first()
    if pincode:
        return _ok({
            'code': pincode.code,
            'city': pincode.city.name,
            'state': pincode.city.state.name,
            'zone': pincode.city.state.zone.name if pincode.city.state.zone else '',
            'country': pincode.city.state.country.name
        })

    return _ok(None, "Pincode not found")
