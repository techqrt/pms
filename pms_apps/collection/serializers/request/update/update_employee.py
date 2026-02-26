from rest_framework import serializers
from pms_apps.collection.dataclasses.request.update.update_employee import CollectionEmployeeUpdateRequest

class ManagerRequestSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()

class CollectionEmployeeUpdateRequestSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    designation = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    region = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    collections_made = serializers.DecimalField(required=False, max_digits=20, decimal_places=2, default=0.00)
    overdue_accounts_handled = serializers.IntegerField(required=False, default=0)
    manager_ref = ManagerRequestSerializer(required=False, allow_null=True)

    def create(self, validated_data) -> CollectionEmployeeUpdateRequest:
        if 'manager_ref' in validated_data and validated_data['manager_ref']:
            manager_ref_data = validated_data.pop('manager_ref')
            validated_data['manager_ref'] = manager_ref_data['manager_id']
        elif 'manager_ref' in validated_data:
            validated_data['manager_ref'] = None

        return CollectionEmployeeUpdateRequest(**validated_data)