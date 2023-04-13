from rest_framework import serializers
from ..models.customers import Customers, CustomerAddress
from ..models.address import Addresses
from system.serializers.common_serializers import *
from system.serializers.user_serializers import RelatedUserSerilaizer
from django.db.models import Q

#**************************Serializer to get the record of addresses in detail**************************#
class RelatedAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addresses
        exclude = ("created_time","modified_time","created_by")

    # To return forign key values in detail 
    def to_representation(self, instance):
        response = super().to_representation(instance)

        state = instance.state
        if state:
            response['state'] = instance.state.system_name
            
        country = instance.country
        if country:
            response['country'] = instance.country.system_name
            
        language = instance.language
        if language:
            response['language'] = instance.language.system_name

        stage = instance.stage
        if stage:
            response['stage'] = instance.stage.system_name

        telephone_type = instance.telephone_type
        if telephone_type:
            response['telephone_type'] = instance.telephone_type.system_name

        other_communication_type = instance.other_communication_type
        if other_communication_type:
            response['other_communication_type'] = instance.other_communication_type.system_name
            
        return response

#**************************Serializer For Customers Model**************************#
class RelatedCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        exclude = ("created_time","modified_time","created_by")

class CustomerSerializer(serializers.ModelSerializer):
    # address = serializers.SerializerMethodField()
    # other_address = serializers.SerializerMethodField()
    
    # def get_address(self,obj):
    #     queryset = CustomerAddress.objects.filter(customer = obj.id)
    #     address_ids = []
    #     for ele in queryset:
    #         address_ids.append(ele.address.id)
    #     address_queryset = Addresses.objects.filter(Q(id__in = address_ids), Q(address_type__system_name = "customer_contact"))
    #     serializer = RelatedAddressSerializer(address_queryset, many = True)         
    #     return serializer.data[0] if serializer.data else None
    
    # def get_other_address(self, obj):
    #     queryset = CustomerAddress.objects.filter(customer = obj.id)
    #     address_ids = []
    #     for ele in queryset:
    #         address_ids.append(ele.address.id)
    #     address_queryset = Addresses.objects.filter(id__in = address_ids).exclude(address_type__system_name = "customer_contact")  
    #     serializer = RelatedAddressSerializer(address_queryset, many = True)         
    #     return serializer.data
    
    class Meta:
        model = Customers 
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time", "created_by")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # To return forign key values in detail     
    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context['request']
        # currency_data = RelatedCurrencySerializer(instance.currency).data
        # if 'id' in currency_data:
        #     response['currency'] = RelatedCurrencySerializer(instance.currency).data
            
        # stage_data = RelatedStageSerializer(instance.stage, context={'request': request}).data
        # if 'id' in stage_data:
        #     response['stage'] = RelatedStageSerializer(instance.stage, context={'request': request}).data
        queryset = CustomerAddress.objects.filter(customer = instance.id)
        if queryset:
            address_ids = []
            for ele in queryset:
                address_ids.append(ele.address.id)
            address_queryset = Addresses.objects.filter(Q(id__in = address_ids), Q(address_type__system_name = "customer_contact"))
            serializer = RelatedAddressSerializer(address_queryset, many = True)
            if serializer:
                address_values = serializer.data
                if address_values:
                    for key, value in address_values[0].items():
                        if key == 'id': pass
                        else: response[key] = value

        stage_data = instance.stage
        if stage_data:
            response['stage']=instance.stage.system_name
            
        created_data = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_data:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data

        parent_data = RelatedCustomerSerializer(instance.parent_id).data
        if 'id' in parent_data:
            response['parent_id'] = RelatedCustomerSerializer(instance.parent_id).data

        shipping_terms = instance.shipping_terms
        if shipping_terms:
            response['shipping_terms'] = instance.shipping_terms.system_name

        entity = instance.entity
        if entity:
            response['entity'] = instance.entity.system_name

        ship_via = instance.ship_via
        if ship_via:
            response['ship_via'] = instance.ship_via.system_name

        payment_terms = instance.payment_terms
        if payment_terms:
            response['payment_terms'] = instance.payment_terms.system_name

        payment_method = instance.payment_method
        if payment_method:
            response['payment_method'] = instance.payment_method.system_name

        customer_source = instance.customer_source
        if customer_source:
            response['customer_source'] = instance.customer_source.system_name

        currency_data = instance.currency
        if currency_data:
            response['currency'] = instance.currency.system_name

        status_data = instance.status
        if status_data:
            response['status'] = instance.status.system_name

        return response

    # pkey of new data will be created on the basis of recordidentifiers. 
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='customers')
        if record_id:
            data['id']=get_rid_pkey('customers')
        return super().create(data)

#**************************Serializer to get the record of addresses related to paricular customer**************************#  
class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        exclude = ("address","id","created_time","modified_time","created_by")
        depth = 1