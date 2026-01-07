from rest_framework import serializers
from pms_apps.finance.dataclasses.request.update.update_manager import FinanceManagerUpdateRequest

class FinanceManagerUpdateRequestSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    dob = serializers.DateField(required=False, allow_null=True)
    department = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    total_budget_managed = serializers.DecimalField(required=False, default=0.0, max_digits=20, decimal_places=2)
    reports_submitted = serializers.IntegerField(required=False, default=0)
    team_size = serializers.IntegerField(required=False, default=0)

    def create(self, validated_data) -> FinanceManagerUpdateRequest:
        return FinanceManagerUpdateRequest(**validated_data)