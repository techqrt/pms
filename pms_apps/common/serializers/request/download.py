from rest_framework import serializers
from pms_apps.common.dataclasses.download import GenerateExcelPDF

class GenerateExcelPDFSerializer(serializers.Serializer):
    module_type = serializers.CharField()
    file_name = serializers.CharField()
    filter_key = serializers.CharField(allow_null=True, required=False, default='')
    filter_value = serializers.CharField(allow_null=True, required=False, default='')
    title = serializers.CharField()
    download_type = serializers.ChoiceField(choices=["pdf", "excel"])

    def create(self, validated_data):
        return GenerateExcelPDF(**validated_data)