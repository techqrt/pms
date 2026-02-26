from rest_framework import serializers
from pms_apps.finance.dataclasses.request.create.create_manager import FinanceManagerCreateRequest

class UserRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

class FinanceManagerCreateRequestSerializer(serializers.Serializer):
    manager_id = UserRequestSerializer()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    department = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    total_budget_managed = serializers.DecimalField(required=False, default=0.0, max_digits=20, decimal_places=2)
    reports_submitted = serializers.IntegerField(required=False, default=0)
    team_size = serializers.IntegerField(required=False, default=0)

    def create(self, validated_data) -> FinanceManagerCreateRequest:
        manger_id_data = validated_data.pop('manager_id')
        validated_data['manager_id'] = manger_id_data['user_id']

        return FinanceManagerCreateRequest(**validated_data)