from rest_framework import viewsets
from ..serializers.entity_serializers import *
from ..models.entity import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from system import utils
from system.models.teams import Team
from sales.serializers.addresses_serializers import AddressSerializer


class EntityViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Company to be modified.
    """
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")

    def create(self, request):
        try:
            data=request.data
            haveBAddr=False
            haveSAddr=False
            haveUser=False
            haveTeam=False
            if "billing_address" in data:
                billing_address= data.pop('billing_address')
                haveBAddr=True
            if "shipping_address" in data:
                shipping_address= data.pop('shipping_address')
                haveSAddr=True
            if "users" in data:
                user_detail = data.pop('users')
                haveUser=True
            if "teams" in data:
                team_detail = data.pop('teams')
                haveTeam = True
            serializer=EntitySerializer(data=data, context={'request':request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                entity_id = serializer.data.get('id')
                new_entity = Entity.objects.get(id = entity_id)
                if haveBAddr == True:
                    new_address = AddressSerializer(data=billing_address, context={'request':request})
                    if new_address.is_valid(raise_exception=True):
                        new_address.save()
                    address_id=new_address.data.get('id')
                    new_address = Addresses.objects.get(id=address_id)
                    create_billing_address=EntityAddress.objects.create(address=new_address,entity=new_entity)
                if haveSAddr == True:
                    new_address = AddressSerializer(data=shipping_address, context={'request':request})
                    if new_address.is_valid(raise_exception=True):
                        new_address.save()
                    address_id=new_address.data.get('id')
                    new_address = Addresses.objects.get(id=address_id)
                    create_shipping_address=EntityAddress.objects.create(address=new_address,entity=new_entity)
                if haveUser == True:
                    for user in user_detail:
                        user = user.get('id')
                        user=User.objects.get(id=user)
                        create_entity_user=EntityUser.objects.create(user=user, entity=new_entity)
                if haveTeam == True:
                    for team in team_detail:
                        team = team.get('id')
                        team=Team.objects.get(id=team)
                        create_Team=EntityTeam.objects.create(team=team, entity=new_entity)     
            company_rec=Entity.objects.get(id=entity_id)
            result=EntitySerializer(company_rec, context={'request':request})
            return Response(utils.success_msg(self,result.data))
        except Exception as e:
            return Response(utils.error(self,str(e)))

    def update(self, request, pk):
        try:
            data=request.data
            haveBAddr=False
            haveSAddr=False
            AddUser=False
            RemoveUser=False
            AddTeam=False
            RemoveTeam=False

            entity_rec = Entity.objects.get(id=pk)
            
            if "billing_address" in data:
                billing_address= data.pop('billing_address')
                haveBAddr=True
            if "shipping_address" in data:
                shipping_address= data.pop('shipping_address')
                haveSAddr=True
            if "add_user" in data:
                add_users=data.pop('add_user')
                AddUser=True
            if "remove_user" in data:
                remove_users= data.pop('remove_user')
                RemoveUser=True
            if "add_team" in data:
                add_teams= data.pop('add_team')
                AddTeam=True
            if "remove_team" in data:
                remove_teams= data.pop('remove_team')
                RemoveTeam=True
            
            serializer=EntitySerializer(entity_rec, data=data, context={'request':request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                if haveBAddr == True:
                    if 'id' in billing_address:
                        address_id=billing_address.get('id')
                        address_rec = Addresses.objects.get(id=address_id)
                        update_address = AddressSerializer(address_rec,data=billing_address, context={'request':request})
                        if update_address.is_valid(raise_exception=True):
                            update_address.save()
                        billing_address=EntityAddress.objects.filter(address=address_id,entity=entity_rec)
                        if not billing_address:
                            create_billing_address=EntityAddress.objects.create(address=new_address,entity=entity_rec)
                    else:
                        new_address = AddressSerializer(data=billing_address, context={'request':request})
                        if new_address.is_valid(raise_exception=True):
                            new_address.save()
                        address_id=new_address.data.get('id')
                        new_address = Addresses.objects.get(id=address_id)
                        create_billing_address=EntityAddress.objects.create(address=new_address,entity=entity_rec)
                if haveSAddr == True:
                    if 'id' in shipping_address:
                        address_id=shipping_address.get('id')
                        address_rec = Addresses.objects.get(id=address_id)
                        update_address = AddressSerializer(address_rec,data=shipping_address, context={'request':request})
                        if update_address.is_valid(raise_exception=True):
                            update_address.save()
                        shipping_address=EntityAddress.objects.filter(address=address_id,entity=entity_rec)
                        if not shipping_address:
                            create_shipping_address=EntityAddress.objects.create(address=new_address,entity=entity_rec)
                    else:
                        new_address = AddressSerializer(data=shipping_address, context={'request':request})
                        if new_address.is_valid(raise_exception=True):
                            new_address.save()
                        address_id=new_address.data.get('id')
                        new_address = Addresses.objects.get(id=address_id)
                        create_shipping_address=EntityAddress.objects.create(address=new_address,entity=entity_rec)
                # Entity updation related to add and remove teams and users
                if AddUser == True:
                    for user in add_users:
                        user = user.get('id')
                        user=User.objects.get(id=user)
                        find = EntityUser.objects.filter(user=user, entity=entity_rec)
                        if not find:
                            add_user=EntityUser.objects.create(user=user, entity=entity_rec)
                if RemoveUser == True:
                    for user in remove_users:
                        user = user.get('id')
                        user=User.objects.get(id=user)
                        find = EntityUser.objects.filter(user=user, entity=entity_rec)
                        if find:
                            remove_user=(EntityUser.objects.filter(user=user, entity=entity_rec)).delete()
                if AddTeam == True:
                    for team in add_teams:
                        team = team.get('id')
                        team=Team.objects.get(id=team)
                        find = EntityTeam.objects.filter(team=team, entuty=entity_rec)
                        if not find:
                            add_Team=EntityTeam.objects.create(team=team, entuty=entity_rec)
                if RemoveTeam == True:
                    for team in remove_teams:
                        team = team.get('id')
                        team=Team.objects.get(id=team)
                        find = EntityTeam.objects.filter(team=team, entuty=entity_rec)
                        if find:
                            remove_Team=(EntityTeam.objects.filter(team=team, entuty=entity_rec)).delete()
            msg = "Entity Updation Successful."
            return Response(utils.success_msg(self,msg))
        except Exception as e:
            return Response(utils.error(self,str(e)))