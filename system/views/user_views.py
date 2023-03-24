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
from sales.serializers.addresses_serializers import AddressSerializer
from system.models.teams import Team
from system.models.roles_permissions import Role, Permission, RolePermissions
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
                    address_rec = data.pop('address')
                    haveAddr = True
                if 'teams' in data:
                    team_rec = data.pop('teams')
                    haveTeam = True
                if 'roles' in data:
                    role_rec = data.pop('roles')
                    haveRoles = True
                serializer = UserSerializer(data=data, context={'request':request})
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    user_id = User.objects.get(id=serializer.data.get('id'))
                    if haveAddr == True:
                        address_rec['address_type'] = 'company user'
                        new_address = AddressSerializer(data=address_rec, context={'request':request})
                        if new_address.is_valid(raise_exception=True):
                            new_address.save()
                        new_address = Addresses.objects.get(id=new_address.data.get('id'))
                        create_user_address=UserAddress.objects.create(address=new_address,user=user_id)
                    if haveTeam == True:
                        for team in team_rec:
                            team = team.get('id')
                            team=Team.objects.get(id=team)
                            create_Team=TeamUser.objects.create(team=team, user=user_id)
                    if haveRoles == True:
                        for role in role_rec:
                            role_id = role.get('id')
                            role_id = Role.objects.get(id=role_id)
                            create_role=UserRoles.objects.create(role=role_id, user=user_id)
                            #permissions = role.get('permissions')
                            #for permission in permissions:
                            #    permission = permission.get('id')
                            #    permission=Permission.objects.get(id=permission)
                            #    check = RolePermissions.objects.create(permissions=permission, role=role_id)
                            #    if check:
                            #        pass
                            #    else:
                            #        create_permission=RolePermissions.objects.create(permissions=permission, role=role_id)
                user_id=serializer.data.get('id')
                new_user = User.objects.get(id=user_id)
                result = UserSerializer(new_user, context={'request':request})
                return Response(utils.success_msg(result.data))
        except Exception as e:
            return Response(utils.error(str(e)))

    def update(self, request, pk):
        try:
            data = request.data
            user_rec = User.objects.get(id=pk)
            haveAddr = False
            AddTeam=False
            RemoveTeam=False
            AddRoles = False
            RemoveRoles = False
            if 'address' in data:
                address_rec = data.pop('address')
                haveAddr = True
            if "add_team" in data:
                add_teams= data.pop('add_team')
                AddTeam=True
            if "remove_team" in data:
                remove_teams= data.pop('remove_team')
                RemoveTeam=True
            if "add_role" in data:
                add_roles= data.pop('add_role')
                AddRoles=True
            if "remove_role" in data:
                remove_roles= data.pop('remove_role')
                RemoveRoles=True
            serializer = UserSerializer(user_rec, data=data, context={'request':request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                user_id = User.objects.get(id=serializer.data.get('id'))
                if haveAddr == True:
                    address_rec['address_type'] = 'company user'
                    check = UserAddress.objects.filter(user=pk)
                    if check:
                        address_id = check.values()[0]['address_id']
                        addr = Addresses.objects.get(id=address_id)
                        update_addr = AddressSerializer(addr, data=address_rec, context={'request':request})
                        if update_addr.is_valid(raise_exception=True):
                            update_addr.save()
                    else:
                        new_address = AddressSerializer(data=address_rec, context={'request':request})
                        if new_address.is_valid(raise_exception=True):
                            new_address.save()
                        new_address = Addresses.objects.get(id=new_address.data.get('id'))
                        create_user_address=UserAddress.objects.create(address=new_address,user=user_id)
                if AddTeam == True:
                    for team in add_teams:
                        team = team.get('id')
                        team=Team.objects.get(id=team)
                        find = TeamUser.objects.filter(team=team, user=user_rec)
                        if not find:
                            add_Team=TeamUser.objects.create(team=team, user=user_rec)
                if RemoveTeam == True:
                    for team in remove_teams:
                        team = team.get('id')
                        team=Team.objects.get(id=team)
                        find = TeamUser.objects.filter(team=team, user=user_rec)
                        if find:
                            remove_Team=(TeamUser.objects.filter(team=team, user=user_rec)).delete()
                        
                if AddRoles == True:
                    for role in add_roles:
                        role = role.get('id')
                        role=Role.objects.get(id=role)
                        find = UserRoles.objects.filter(role=role, user=user_rec)
                        if not find:
                            add_role=UserRoles.objects.create(role=role, user=user_rec)
                if RemoveRoles == True:
                    for role in remove_roles:
                        role = role.get('id')
                        role=Role.objects.get(id=role)
                        find = UserRoles.objects.filter(role=role, user=user_rec)
                        if find:
                            remove_role=(UserRoles.objects.filter(role=role, user=user_rec)).delete()
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
            user_id = serializers.data.get('user_id')
            curr_pass = serializers.data.get('current_password')
            new_password = serializers.data.get('new_password')
            user = User.objects.get(id=user_id)
            if user:
                password = user.password
                if check_password(curr_pass, password):
                    user.set_password(new_password)
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
             token = serializers.validate(request.data)['token']
             response = {'status': 'success','code': status.HTTP_200_OK,'message': msg, 'token': token}
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
