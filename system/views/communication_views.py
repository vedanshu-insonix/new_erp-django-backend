from rest_framework import viewsets
from ..serializers.communication_serializers import *
from ..models.communication import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status


class ChannelViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Buttons to be modified.
    """
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
    
class CommunicationViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Buttons to be modified.
    """
    queryset = Communication.objects.all()
    serializer_class = CommunicationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")

    def create(self, request):
        try:
            new_comm = request.data
            address = None
            if 'address' in new_comm:
                address = new_comm.pop('address')
            serializer = CommunicationSerializer(data=new_comm, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            if address:
                new_comm_addr = CommunicationAddress.objects.create(created_by_id = request.user.id,
                                                                    communication_id = serializer.data.get('id'),
                                                                    address_id=address)
                if new_comm.get('primary') == True:
                    new_comm_addr = CommunicationAddress.objects.get(id=new_comm_addr.id)
                    channel_type=new_comm.get('communication_channel')
                    if channel_type=='telephone':
                        address_rec = Address.objects.filter(id=new_comm_addr.address_id).update(telephone = new_comm.get('external_routing'),
                                                                                            telephone_type = new_comm.get('communication_type'),
                                                                                            type = 'communication')
                    elif channel_type=='email':
                        address_rec = Address.objects.filter(id=new_comm_addr.address_id).update(email = new_comm.get('external_routing'),
                                                                                            type = 'communication')
                    else:
                        pass                                        
            return Response({"msg":serializer.data,
                            "status":"success",
                            "code":status.HTTP_201_CREATED})
        except Exception as e:
            return Response({"msg":"Unable to create new communication record",
                            "reason":str(e),
                            "status":"failed",
                            "code":status.HTTP_400_BAD_REQUEST})