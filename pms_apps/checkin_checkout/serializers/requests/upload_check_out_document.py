from rest_framework import serializers

from pms_apps.checkin_checkout.models.check_out_document import CheckOutDocument
from pms_apps.checkin_checkout.dataclasses.requests.upload_check_out_document import CheckOutDocumentUploadRequest


class CheckOutDocumentUploadSerializer(serializers.Serializer):
    check_out_id = serializers.IntegerField()
    document_type = serializers.ChoiceField(
        choices=[choice[0] for choice in CheckOutDocument.DOCUMENT_TYPE_CHOICES]
    )
    file = serializers.CharField()
    document_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    linked_to_label = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    expiry_date = serializers.DateField(required=False, allow_null=True)

    def create(self, validated_data) -> CheckOutDocumentUploadRequest:
        return CheckOutDocumentUploadRequest(
            check_out_id=validated_data['check_out_id'],
            document_type=validated_data['document_type'],
            file=validated_data['file'],
            document_name=validated_data.get('document_name'),
            linked_to_label=validated_data.get('linked_to_label'),
            expiry_date=validated_data.get('expiry_date'),
        )
