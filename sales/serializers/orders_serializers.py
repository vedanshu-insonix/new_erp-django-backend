from rest_framework import serializers
from sales.models.sales_orders import *
from system.serializers.user_serializers import RelatedUserSerilaizer
from system.serializers.common_serializers import *
from sales.serializers.addresses_serializers import AddressSerializer
from sales.serializers.customers_serializers import RelatedCustomerSerializer

class RelatedSalesOrdersSerializer(serializers.ModelSerializer):
     class Meta:
        model = SalesOrders
        fields = ("__all__")

class SalesOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrders
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context['request']
        customer = RelatedCustomerSerializer(instance.customer,context={'request': request}).data
        if 'id' in customer:
            response['customer'] = RelatedCustomerSerializer(instance.customer, context={'request': request}).data

        contact_address = AddressSerializer(instance.contact_address, context={'request': request}).data
        if 'id' in contact_address:
            response['contact_address'] = AddressSerializer(instance.contact_address, context={'request': request}).data

        billing_address = AddressSerializer(instance.billing_address, context={'request': request}).data
        if 'id' in billing_address:
            response['billing_address'] = AddressSerializer(instance.billing_address, context={'request': request}).data

        billing_state = RelatedStateSerializer(instance.billing_state, context={'request': request}).data
        if 'id' in billing_state:
            response['billing_state'] = RelatedStateSerializer(instance.billing_state, context={'request': request}).data

        billing_country = RelatedCountrySerializer(instance.billing_country, context={'request': request}).data
        if 'id' in billing_country:
            response['billing_country'] = RelatedCountrySerializer(instance.billing_country, context={'request': request}).data

        shipping_address = AddressSerializer(instance.shipping_address, context={'request': request}).data
        if 'id' in shipping_address:
            response['shipping_address'] = AddressSerializer(instance.shipping_address, context={'request': request}).data

        shipping_state = RelatedStateSerializer(instance.shipping_state, context={'request': request}).data
        if 'id' in shipping_state:
            response['shipping_state'] = RelatedStateSerializer(instance.shipping_state, context={'request': request}).data

        shipping_country = RelatedCountrySerializer(instance.shipping_country, context={'request': request}).data
        if 'id' in shipping_country:
            response['shipping_country'] = RelatedCountrySerializer(instance.shipping_country, context={'request': request}).data
        
        accepted_currency = RelatedCurrencySerializer(instance.accepted_currency, context={'request': request}).data
        if 'id' in accepted_currency:
            response['accepted_currency'] = RelatedCurrencySerializer(instance.accepted_currency, context={'request': request}).data

        order_stage = RelatedStageSerializer(instance.order_stage, context={'request': request}).data
        if 'id' in order_stage:
            response['order_stage'] = RelatedStageSerializer(instance.order_stage, context={'request': request}).data

        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data

        return response
    
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='salesorders')
        if record_id:
            data['id']=get_rid_pkey('salesorders')
        return super().create(data)

class SalesOrderLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrderLines
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='salesorderlines')
        if record_id:
            data['id']=get_rid_pkey('salesorderlines')
        return super().create(data)
