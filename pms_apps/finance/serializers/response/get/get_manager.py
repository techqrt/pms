from rest_framework import serializers


class UserGetSerializer(serializers.Serializer):
    userId = serializers.IntegerField()
    phoneNumber = serializers.CharField()
    email = serializers.EmailField()


class FinanceManagerGetSerializer(serializers.Serializer):
    managerId = UserGetSerializer(read_only=True)
    name = serializers.CharField(read_only=True)
    dob = serializers.DateField(read_only=True)
    department = serializers.CharField(read_only=True)
    totalBudgetManaged = serializers.DecimalField(read_only=True, max_digits=20, decimal_places=2)
    teamSize = serializers.IntegerField(read_only=True)
    reportsSubmitted = serializers.IntegerField(read_only=True)
    createdAt = serializers.DateTimeField(read_only=True)


class FinanceManagerResponseGetSerializer(serializers.Serializer):
    data = FinanceManagerGetSerializer(read_only=True)
