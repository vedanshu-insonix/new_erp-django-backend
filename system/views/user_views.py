from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.hashers import check_password
from rest_framework import status
from ..models.users import *
from ..serializers.user_serializers import *
from ..serializers.common_serializers import RelatedConfigurationSerializer
from ..views.common_views import get_tokens_for_user
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from system import utils
from system.models.common import Choice
from sales.serializers.addresses_serializers import AddressSerializer
from system.models.teams import Team
from system.models.roles_permissions import Role, Permission
from rest_framework.decorators import  permission_classes, authentication_classes
from rest_framework.permissions import AllowAny

class UserViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows users to be modified.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")

    def create(self, request):
        try:
            data = request.data
            email= data.get("email")
            haveAddr = False
            haveTeam = False
            haveRoles = False           
            user=User.objects.filter(email=email) 
            if user:
                return Response(utils.error("User Already Exist With This Email Id"))
            else:
                if 'address' in data:
                    addressRec = data.pop('address')
                    haveAddr = True
                if 'teams' in data:
                    teamRec = data.pop('teams')
                    haveTeam = True
                if 'roles' in data:
                    roleRec = data.pop('roles')
                    haveRoles = True
                serializer = UserSerializer(data=data, context={'request':request})
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    userId = User.objects.get(id=serializer.data.get('id'))
                    if haveAddr == True:
                        addressRec['address_type'] = Choice.objects.get(id='8012')
                        addressRec['user'] = userId
                        newAddress = AddressSerializer(data=addressRec, context={'request':request})
                        if newAddress.is_valid(raise_exception=True):
                            newAddress.save()
                        newAddress = Addresses.objects.get(id=newAddress.data.get('id'))
                        # create_user_address=UserAddress.objects.create(address=new_address,user=user_id)
                    if haveTeam == True:
                        for team in teamRec:
                            teamId = team.get('id')
                            teamId=Team.objects.get(id=teamId)
                            createTeam=TeamUser.objects.create(team=teamId, user=userId)
                    if haveRoles == True:
                        for role in roleRec:
                            roleId = role.get('id')
                            roleId = Role.objects.get(id=roleId)
                            createRole=UserRoles.objects.create(role=roleId, user=userId)
                userId=serializer.data.get('id')
                newUser = User.objects.get(id=userId)
                result = UserSerializer(newUser, context={'request':request})
                return Response(utils.success_msg(result.data))
        except Exception as e:
            return Response(utils.error(str(e)))

    def update(self, request, pk):
        try:
            data = request.data
            userRec = User.objects.get(id=pk)
            haveAddr = False
            addTeam=False
            delTeam=False
            addRoles = False
            delRoles = False
            if 'address' in data:
                addressRec = data.pop('address')
                haveAddr = True
            if "add_team" in data:
                newTeams= data.pop('add_team')
                addTeam=True
            if "remove_team" in data:
                teams= data.pop('remove_team')
                delTeam=True
            if "add_role" in data:
                newRoles= data.pop('add_role')
                addRoles=True
            if "remove_role" in data:
                roles= data.pop('remove_role')
                delRoles=True
            if 'password' in data:
                msg = "Password Can't be updated through this interface. Please Request a Reset Password Email from Admin."
                return Response(utils.error(msg))
            else:
                serializer = UserSerializer(userRec, data=data, context={'request':request})
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    userId = User.objects.get(id=serializer.data.get('id'))
                    if haveAddr == True:
                        addressRec['address_type'] = Choice.objects.get(id='8012')
                        check = Addresses.objects.filter(user=pk)
                        if check:
                            address_id = check.values()[0]['id']
                            addr = Addresses.objects.get(id=address_id)
                            editAddr = AddressSerializer(addr, data=addressRec, context={'request':request})
                            if editAddr.is_valid(raise_exception=True):
                                editAddr.save()
                        else:
                            addressRec['user']=userId
                            newAddress = AddressSerializer(data=addressRec, context={'request':request})
                            if newAddress.is_valid(raise_exception=True):
                                newAddress.save()
                            # new_address = Addresses.objects.get(id=new_address.data.get('id'))
                            # create_user_address=UserAddress.objects.create(address=new_address,user=user_id)
                    if addTeam == True:
                        for team in newTeams:
                            team = team.get('id')
                            team=Team.objects.get(id=team)
                            find = TeamUser.objects.filter(team=team, user=userId)
                            if not find:
                                addTeams=TeamUser.objects.create(team=team, user=userId)
                    if delTeam == True:
                        for team in teams:
                            team = team.get('id')
                            team=Team.objects.get(id=team)
                            find = TeamUser.objects.filter(team=team, user=userId)
                            if find:
                                delTeams=(TeamUser.objects.filter(team=team, user=userId)).delete()
                            
                    if addRoles == True:
                        for role in newRoles:
                            role = role.get('id')
                            role=Role.objects.get(id=role)
                            find = UserRoles.objects.filter(role=role, user=userId)
                            if not find:
                                addRole=UserRoles.objects.create(role=role, user=userId)
                    if delRoles == True:
                        for role in roles:
                            role = role.get('id')
                            role=Role.objects.get(id=role)
                            find = UserRoles.objects.filter(role=role, user=userId)
                            if find:
                                delRole=(UserRoles.objects.filter(role=role, user=userId)).delete()
                msg = "User Updation Successful."
                return Response(utils.success_msg(msg))
        except Exception as e:
            return Response(utils.error(str(e)))

    # User login API
    @action(detail=False, methods=['post'], name='login')
    def login(self, request,*args, **kwargs):
        serializers = UserLoginSerializer(data = request.data)
        if serializers.is_valid(raise_exception=True):
            username = request.data.get('username')
            entity = request.data.get('entity')
            password = request.data.get('password')
            # user = authenticate(email= email, password=password)
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                token = get_tokens_for_user(user)
                msg = 'Login Successful!'
                # queryset = Configuration.objects.filter(category = "appearance")
                #queryset = Configuration.objects.filter(system_name = "appearance")
                #configuration = RelatedConfigurationSerializer(queryset, many = True)
                response = {'status': 'success','code': status.HTTP_200_OK,'message': msg, 'token':token, "username":username} #, "configuration":configuration.data}
                return Response(response)
            else:
                msg = 'Username or Password is not valid'
                response = {'status': 'error','code': status.HTTP_404_NOT_FOUND,'message': msg}
                return Response(response)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Change Password
    @action(detail=False, methods=['post'], url_path = "change-password")
    def changePassword(self, request):
        serializers = ChangePasswordSerializer(data = request.data)
        if serializers.is_valid(raise_exception=True):
            userId = serializers.data.get('user_id')
            currPass = serializers.data.get('current_password')
            newPassword = serializers.data.get('new_password')
            user = User.objects.get(id=userId)
            if user:
                password = user.password
                if check_password(currPass, password):
                    user.set_password(newPassword)
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

    # Send link to Reset Password
    @action(detail=False, methods=['post'], url_path='request-reset-email', url_name='request-reset-email')
    def request_reset_email(self, request):
        serializers = SendPasswordResetEmailSerializer(data=request.data, context = {'request': request})
        if serializers.is_valid(raise_exception=True):
            msg = "Password Reset link send. Please check your email"
            response = {'status': 'success','code': status.HTTP_200_OK,'message': msg}
            return Response(response)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Reset Password 
    @action(detail=False, methods=['post'],url_path = "reset-password/(?P<uid>[-\w]+)_(?P<token>[-\w]+)")
    def resetPassword(self, request, uid, token):
        serializers = UserPasswordResetSerializer(data = request.data, context = {'uid':uid, 'token': token})
        if serializers.is_valid(raise_exception=True):
            msg = "Password Reset successfully"
            response = {'status': 'success','code': status.HTTP_200_OK,'message': msg}
            return Response(response)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_permissions(self):
        """Returns the permission based on the type of action"""

        actions = ["request_reset_email", "resetPassword", "login"]

        if self.action in actions :
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]
        
class GroupViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows groups to be modified.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("__all__")    
