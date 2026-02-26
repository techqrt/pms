from rest_framework import serializers
from pms_apps.collection.dataclasses.request.create.create_manager import CollectionManagerCreateRequest

class UserRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

class CollectionManagerCreateRequestSerializer(serializers.Serializer):
    manager_id = UserRequestSerializer()
    name = serializers.CharField(max_length=255)
    dob = serializers.DateField(required=False, allow_null=True)
    department = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    total_collections = serializers.DecimalField(max_digits=20, decimal_places=2, required=False, default=0.00)
    overdue_accounts_managed = serializers.IntegerField(required=False, default=0)
    team_size = serializers.IntegerField(required=False, default=0)

    def create(self, validated_data) -> CollectionManagerCreateRequest:
        manger_id_data = validated_data.pop('manager_id')
        validated_data['manager_id'] = manger_id_data['user_id']

        return CollectionManagerCreateRequest(**validated_data)