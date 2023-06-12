from rest_framework import viewsets
from ..serializers.communication_serializers import *
from ..models.communication import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from system import utils


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
            newComm = request.data
            address = None
            if 'address' in newComm:
                address = newComm.pop('address')
            serializer = CommunicationSerializer(data=newComm, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            commId = Communication.objects.get(id=serializer.data.get('id'))
            addrID = commId.address.all()
            if (newComm.get('primary') == True) and addrID:
                addr = Addresses.objects.filter(id__in=addrID)
                if addr:
                    channelType=newComm.get('communication_channel')
                    if channelType=='telephone':
                        addressRec = addr.update(telephone = newComm.get('external_routing'), telephone_type = newComm.get('communication_type'))
                    elif channelType=='email':
                        addressRec = addr.update(email = newComm.get('external_routing'))
                    else:
                        pass    
            result = serializer.data                                    
            return Response(utils.success_msg(result))
        except Exception as e:
            return Response(utils.error(str(e)))