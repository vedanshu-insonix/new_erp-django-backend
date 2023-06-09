from asyncore import write
from xml.dom import ValidationErr
from django.contrib.auth.models import User, Group
from system.models.common import Configuration
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.conf import settings
from system.utils import send_email
from system.models.teams import TeamUser
from system.serializers.team_serializer import TeamUserSerializer
from system.models.users import UserAddress, UserRoles

#**************************Serializer For User Model**************************#
class RelatedUserSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =("id","first_name", "last_name", "email")

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    teams = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

    def get_teams(self, obj):
        queryset = TeamUser.objects.filter(user=obj.id)
        serializer = TeamUserSerializer(queryset, many=True)
        result=[]
        for i in range(len(serializer.data)):
            result.append(serializer.data[i]['team']) if serializer.data else None
        return result

    def get_address(self, obj):
        queryset = UserAddress.objects.filter(user=obj.id)
        serializer = UserAddressSerilaizer(queryset, many=True)
        result=[]
        for i in range(len(serializer.data)):
            result.append(serializer.data[i]['address']) if serializer.data else None
        return result
        
    def get_roles(self, obj):
        queryset = UserRoles.objects.filter(user = obj.id)
        serializer = UserRoleSerilaizer(queryset, many=True)
        result=[]
        for i in range(len(serializer.data)):
            result.append(serializer.data[i]['role']) if serializer.data else None
        return result

    class Meta:
        model = User
        fields = ("__all__")
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)

#**************************Serializer For User Address Model**************************#
class UserAddressSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        exclude =("id","user", "created_time", "modified_time", "created_by")
        depth = 1

#**************************Serializer For User Roles Model**************************#
class UserRoleSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = UserRoles
        exclude =("id","user", "created_time", "modified_time", "created_by")
        depth = 1

#**************************Serializer For Group Model**************************#
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("__all__")

#**************************Serializer For User Login Functionality**************************#        
class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length = 255)    
    class Meta:
        model = User
        fields = ["username","password"]

#**************************Serializer For Change Password Functionality**************************#        
class ChangePasswordSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields =["user_id","current_password","new_password"]

#**************************Serializer For Send Email Functionality**************************#
class SendPasswordResetEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)

    class Meta:
        model = User
        fields = ['email']
       
    def validate(self, attrs):
        email = attrs.get('email')
        request = self.context.get('request')

        if User.objects.filter(email = email).exists():
            user = User.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            #base_uri = str('/'.join(request.build_absolute_uri().split('/')[:-2]))
            base_uri = "http://localhost:3000"
            full_token = uid+'_'+token
            link =  base_uri + '/reset-password/' +  full_token + '/'
            # Send Email
            email_from = settings.EMAIL_HOST_USER
            subject = "Password Reset Requested"
            attrs['token'] = full_token
            content='Set your new password by clicking on the below link. Thank You :)'
            message = f'{content} \n {link}'
            status = send_email(subject,message,email)
            if status == "0":
                raise ValidationError('Email sending failed. Please try again')
            return attrs
        else:
            raise ValidationError('You are not registered user.')

#**************************Serializer For Reset Password Functionality**************************#
class UserPasswordResetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 255, style = {'input_type':'password'}, write_only = True)
    confirm_password = serializers.CharField(max_length = 255, style = {'input_type':'password'}, write_only = True)
    
    class Meta: 
        model = User
        fields = ['password', 'confirm_password']
        
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            confirm_password = attrs.get("confirm_password")
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != confirm_password:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user= User.objects.get(id = id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationError("Token is not valid or Expired")
            user.set_password(password)
            user.save()        
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError('Token is not valid or Expired')
    