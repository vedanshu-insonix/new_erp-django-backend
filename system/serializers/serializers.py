from xml.dom import ValidationErr
from django.contrib.auth.models import User, Group
from sales.models.customers import Customer
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ("__all__")
        
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("__all__")
        

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ["email","password"]
        
class ChangePasswordSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields =["user_id","current_password","new_password"]


class SendPasswordResetEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email = email).exists():
            user = User.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print(uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print(token)
            link = 'http://127.0.0.1:8000/api/user/reset/' + uid + '/'+ token
            print(link)
            # Send Email
            return attrs
        else:
            raise ValidationErr('You are not registered user.')
        
