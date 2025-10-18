from rest_framework import status
from rest_framework.decorator import api_view , permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from apps.users.models import User


@api_view(POST)
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({
            'error':'Email and password are required'},
             status=status.HTTP_400_BAD_REQUEST
        )
    user = authenticate(username = email, password = password)
    if user and user.is_active:
        refresh = RefreshToken.for_user(user)
        return Response({
            'acces': str(refresh.access_token),
            'refresh': str(refresh),
            'user':{
                'id':user.id,
                'email':user.email,
                'first_name': user.first_name,
                'username':user.username,
                'last_name':user.last_name,
            }
        })
    
    
    return Respone({
        'error':'Invalid credentials'},
        status = status.HTTP_401_UNAUTHORIZED
    )


@api_view(POST)
@permission_classes([AllowAny])
def refresh_token(request):
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Respone(
                {'error':'Refresh token is required'},
                            status = status.HTTP_400_BAD_REQUEST)
        refrest = RefreshToken(refresh_token)
        return Respone({
                'access':str('refresh.access_token'),
                })

    except Exception as e:
        return Respone({
        'error':'Invalid refresh token'},
        status = status.HTTP_401_UNAUTHORIZED)
    
    


