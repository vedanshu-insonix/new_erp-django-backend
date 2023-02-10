from rest_framework import serializers
from system.models.dataset import Table, Data
from system.serializers.user_serializers import RelatedUserSerilaizer

class RelatedTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        exclude =("created_by", "created_time", "modified_time", "description")

class TableSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        table_id = obj.id
        data_queryset = Data.objects.filter(table = table_id)
        serializer = DataSerializer(data_queryset, many = True)         
        return serializer.data
        
    class Meta:
        model = Table
        fields =("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}} 

    def to_representation(self, instance):
        response = super().to_representation(instance)

        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        exclude =("created_time", "modified_time", "created_by")