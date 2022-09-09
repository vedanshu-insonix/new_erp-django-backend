from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.hashers import check_password
from rest_framework import status
from sales.models.customers import Customer
from ..serializers.user_serializers import UserSerializer, GroupSerializer, UserLoginSerializer, ChangePasswordSerializer, SendPasswordResetEmailSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from ..views.common_views import get_tokens_for_user

class UserViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows users to be modified.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # User login API
    @action(detail=False, methods=['post'], name='login')
    def login(self, request,*args, **kwargs):
        serializers = UserLoginSerializer(data = request.data)
        if serializers.is_valid(raise_exception=True):
            email = request.data.get('email')
            password = request.data.get('password')
            # user = authenticate(email= email, password=password)
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                token = get_tokens_for_user(user)
                msg = 'Login Successful!'
                response = {'status': 'success','code': status.HTTP_200_OK,'message': msg, 'token':token}
                return Response(response)
            else:
                msg = 'Email or Password is not valid'
                response = {'status': 'error','code': status.HTTP_404_NOT_FOUND,'message': msg}
                return Response(response)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Change Password
    @action(detail=False, methods=['post'], name='changePassword')
    def changePassword(self, request):
        serializers = ChangePasswordSerializer(data = request.data)
        if serializers.is_valid(raise_exception=True):
            user_id = serializers.data.get('user_id')
            curr_pass = serializers.data.get('current_password')
            password = serializers.data.get('new_password')
            user = User.objects.get(id=user_id)
            if user:
                password = user.password
                if check_password(curr_pass, password):
                    user.set_password(password)
                    user.save()
                    msg = "Password changed successfully!"
                    response = {'status': 'success','code': status.HTTP_200_OK,'message': msg}
                    return Response(response)
                else:
                    msg = "Enter a valid password and try again!"
                    response = {'status': 'error','code': status.HTTP_200_OK,'message': msg}
                    return Response(response)
            else:
                msg = "User not found!"
                response = {'status': 'error','code': status.HTTP_404_NOT_FOUND,'message': msg}
                return Response(response)     
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    # Reset Password
    @action(detail=False, methods=['post'], name='resetPassword')
    def resetPassword(self, request):
         serializers = SendPasswordResetEmailSerializer(data = request.data)
         if serializers.is_valid(raise_exception=True):
             return Response({'message':'Password Reset link send. Please check your email'}, status=status.HTTP_200_OK)
         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
     
class GroupViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows groups to be modified.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    
