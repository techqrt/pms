from rest_framework import serializers

from pms_apps.checkin_checkout.models.check_in_document import CheckInDocument
from pms_apps.checkin_checkout.dataclasses.requests.upload_check_in_document import CheckInDocumentUploadRequest


class CheckInDocumentUploadSerializer(serializers.Serializer):
    check_in_id = serializers.IntegerField()
    document_type = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckInDocument.DOCUMENT_TYPE_CHOICES]
    )
    file = serializers.CharField()
    linked_to_label = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    expiry_date = serializers.DateField(required=False, allow_null=True)

    def create(self, validated_data) -> CheckInDocumentUploadRequest:
        return CheckInDocumentUploadRequest(
            check_in_id=validated_data['check_in_id'],
            document_type=validated_data['document_type'],
            file=validated_data['file'],
            linked_to_label=validated_data.get('linked_to_label'),
            expiry_date=validated_data.get('expiry_date'),
        )
