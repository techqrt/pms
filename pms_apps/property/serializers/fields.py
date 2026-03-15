from rest_framework import serializers


class Base64ImageField(serializers.Field):
    """
    Custom field to handle base64 encoded images or URLs.
    Accepts:
    - base64 strings (with or without data: prefix)
    - HTTP(S) URLs
    
    Passes the data through to be processed later by ImageUtils.
    """
    
    def to_representation(self, value):
        """Convert file object to URL string for response"""
        if not value:
            return None
        
        # Return the URL representation
        if hasattr(value, 'url'):
            return value.url
        return str(value)
    
    def to_internal_value(self, data):
        """Validate and pass through the image data (base64 or URL)"""
        if not data:
            return None
        
        if not isinstance(data, str):
            raise serializers.ValidationError("Image data must be a string (base64 or URL)")
        
        # Validate it's either a URL or looks like base64
        if data.startswith('http://') or data.startswith('https://'):
            # It's a URL, pass it through
            return data
        elif data.startswith('data:') or len(data) > 50:  # Likely a base64 string
            # It's likely base64, pass it through for processing by ImageUtils
            return data
        else:
            raise serializers.ValidationError(
                "Image data must be either a valid base64 string or an HTTP(S) URL"
            )
