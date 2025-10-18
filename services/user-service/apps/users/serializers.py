from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from .models import User, UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name',
            'is_active', 'date_joined']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'date_of_birth']

class UserWithProfileSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name',
            'last_name', 'is_active', 'date_joined', 'profile']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name',
            'last_name', 'password', 'password_confirm']
    

    def validate(self, attrs):
        if attrs['passowrd'] != attrs['password confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs    

    def create(self,validated_data):
        validated_data.pop('password confirm')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user