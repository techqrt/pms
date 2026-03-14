import base64
import uuid
from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.Field):
    """
    Custom field to handle base64 encoded images.
    Accepts base64 strings and converts them to Django File objects.
    """
    
    def to_representation(self, value):
        """Convert file object to base64 string for response"""
        if not value:
            return None
        
        try:
            with value.open('rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
        except:
            return None
    
    def to_internal_value(self, data):
        """Convert base64 string to file object"""
        if isinstance(data, str):
            # Already a URL or file path (handle from GET response)
            return data
        
        if not data:
            return None
        
        # Assume it's base64 encoded
        try:
            # data can be in format: "data:image/jpeg;base64,/9j/4AAQSkZJRg..." or just the base64 string
            if isinstance(data, str) and data.startswith('data:'):
                # Extract base64 part after comma
                _, base64_str = data.split(',', 1)
            else:
                base64_str = data
            
            # Decode base64
            decoded_data = base64.b64decode(base64_str)
            
            # Create a file with a unique name
            filename = f"property_photo_{uuid.uuid4()}.jpg"
            
            # Return file-like object
            return ContentFile(decoded_data, name=filename)
        
        except Exception as e:
            raise serializers.ValidationError(f"Invalid base64 image data: {str(e)}")
