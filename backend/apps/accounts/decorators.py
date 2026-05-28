from functools import wraps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

def verify_bearer_token(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'status': False, 'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token_key = auth_header.split('Bearer ')[1].strip()
        try:
            token = Token.objects.select_related('user').get(key=token_key)
            request.user = token.user
        except Token.DoesNotExist:
            return Response({'status': False, 'message': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
            
        return view_func(request, *args, **kwargs)
        
    return _wrapped_view
