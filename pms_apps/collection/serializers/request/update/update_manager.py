from rest_framework import serializers
from pms_apps.collection.dataclasses.request.update.update_manager import CollectionManagerUpdateRequest

class CollectionManagerUpdateRequestSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    dob = serializers.DateField(required=False, allow_null=True)
    department = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    total_collections = serializers.DecimalField(max_digits=20, decimal_places=2, required=False, default=0.00)
    overdue_accounts_managed = serializers.IntegerField(required=False, default=0)
    team_size = serializers.IntegerField(required=False, default=0)

    def create(self, validated_data) -> CollectionManagerUpdateRequest:
        return CollectionManagerUpdateRequest(**validated_data)