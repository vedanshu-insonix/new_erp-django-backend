from rest_framework import viewsets
from system.models.teams import *
from system.serializers.team_serializer import *
from rest_framework.response import Response
from system import utils
from system.models.roles_permissions import Role

class TeamViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Team to be modified.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def create(self,request):
        try:
            data=request.data
            haveUser = False
            haveRole = False

            if 'users' in data:
                users = data.pop('users')
                haveUser = True
            if 'roles' in data:
                roles = data.pop('roles')
                haveRole = True
            
            serializer = TeamSerializer(data=data, context={'request':request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                team_id=serializer.data.get('id')
                new_team = Team.objects.get(id=team_id)
                if haveUser == True:
                    for user in users:
                        user = user.get('id')
                        user=User.objects.get(id=user)
                        create_company_user=TeamUser.objects.create(user=user, team=new_team)
                if haveRole == True:
                    for role in roles:
                        role_id = role.get('id')
                        role_id = Role.objects.get(id=role_id)
                        create_role=TeamRole.objects.create(role=role_id, team=new_team)
                        #permissions = role.get('permissions')
                        #for permission in permissions:
                        #    permission_id = permission.get('id')
                        #    permission=Permission.objects.get(id=permission_id)
                        #    check = RolePermissions.objects.filter(permissions=permission, role=role_id)
                        #    if check:
                        #        pass
                        #    else:
                        #        create_permission=RolePermissions.objects.create(permissions=permission, role=role_id)
                new_team = Team.objects.get(id=team_id)
                result = TeamSerializer(new_team, context={'request':request})
                return Response(utils.success_msg(result.data))
        except Exception as e:
            return Response(utils.error(str(e)))

    def update(self, request, pk):
        try:
            data = request.data
            team_rec = Team.objects.get(id=pk)
            AddUser=False
            RemoveUser=False
            AddRoles = False
            RemoveRoles = False
            
            if "add_role" in data:
                add_roles= data.pop('add_role')
                AddRoles=True
            if "remove_role" in data:
                remove_roles= data.pop('remove_role')
                RemoveRoles=True
            if "add_user" in data:
                add_users=data.pop('add_user')
                AddUser=True
            if "remove_user" in data:
                remove_users= data.pop('remove_user')
                RemoveUser=True

            serializer = TeamSerializer(team_rec, data=data, context={'request':request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                if AddRoles == True:
                    for role in add_roles:
                        role = role.get('id')
                        role=Role.objects.get(id=role)
                        find = TeamRole.objects.filter(role=role, team=team_rec)
                        if not find:
                            add_role=TeamRole.objects.create(role=role, team=team_rec)
                if RemoveRoles == True:
                    for role in remove_roles:
                        role = role.get('id')
                        role=Role.objects.get(id=role)
                        find = TeamRole.objects.filter(role=role, team=team_rec)
                        if find:
                            remove_role=(TeamRole.objects.filter(role=role, team=team_rec)).delete()
                if AddUser == True:
                    for user in add_users:
                        user = user.get('id')
                        user=User.objects.get(id=user)
                        find = TeamUser.objects.filter(user=user, team=team_rec)
                        if not find:
                            add_user=TeamUser.objects.create(user=user, team=team_rec)
                if RemoveUser == True:
                    for user in remove_users:
                        user = user.get('id')
                        user=User.objects.get(id=user)
                        find = TeamUser.objects.filter(user=user, team=team_rec)
                        if find:
                            remove_user=(TeamUser.objects.filter(user=user, team=team_rec)).delete()
                msg = "Team Updation Successful."
            return Response(utils.success_msg(msg))
        except Exception as e:
            return Response(utils.error(str(e)))

class TeamRoleViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows TeamRole to be modified.
    """
    queryset = TeamRole.objects.all()
    serializer_class = TeamRoleSerializer

class TeamUserViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows TeamUser to be modified.
    """
    queryset = TeamUser.objects.all()
    serializer_class = TeamUserSerializer