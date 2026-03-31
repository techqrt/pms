from rest_framework import serializers


class PropertyAssignmentGetSerializer(serializers.Serializer):
    property_assignment_id = serializers.IntegerField()

    @staticmethod
    def get_parameters():
        return [
            {
                "name": "property_assignment_id",
                "in": "query",
                "required": True,
                "schema": {"type": "integer"},
                "description": "Property Assignment ID"
            }
        ]
