from rest_framework import serializers
from warehouse.models.general import *
from system.serializers.user_serializers import RelatedUserSerilaizer
from system.service import get_rid_pkey
from system.models.recordid import RecordIdentifiers

#**************************Serializer For Journal Model**************************#
class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='journal')
        if record_id:
            data['id']=get_rid_pkey('journal')
        return super().create(data)

#**************************Serializer For Journal Template Model**************************#
class RelatedJournalTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalTemplate
        exclude = ("created_time","modified_time","created_by")

class JournalTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalTemplate
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
    
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)

        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
            
        return response
    
    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='journaltemplate')
        if record_id:
            data['id']=get_rid_pkey('journaltemplate')
        return super().create(data)

#**************************Serializer For Attributes Model**************************#
class RelatedAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attributes
        exclude = ("created_time","modified_time","created_by")

class AttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attributes
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
    
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
            
        return response
    
    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='attributes')
        if record_id:
            data['id']=get_rid_pkey('attributes')
        return super().create(data)

#**************************Serializer For Product Attribute Model**************************#
# class ProductAttributeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductAttribute
#         exclude = ("id","product","created_time","modified_time","created_by")
#         depth = 1
        
#**************************Serializer For Images Model**************************#
class RelatedImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        exclude = ("created_time","modified_time","created_by")

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
    
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)

        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
            
        return response
    
    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='images')
        if record_id:
            data['id']=get_rid_pkey('images')
        return super().create(data)

#**************************Serializer For Product Images Model**************************#
# class ProductImagesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductImages
#         exclude = ("id","product","created_time","modified_time","created_by")
#         depth = 1

#**************************Serializer For Value Model**************************#
class RelatedValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Values
        exclude = ("created_time","modified_time","created_by")

class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Values
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
    
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)

        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response
    
    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='value')
        if record_id:
            data['id']=get_rid_pkey('value')
        return super().create(data)