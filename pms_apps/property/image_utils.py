import base64
import uuid
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


class ImageUtils:
    """Utility class for handling image uploads and base64 conversions"""
    
    @staticmethod
    def process_photo(photo_data, upload_path="property_photos/"):
        """
        Process a photo that can be either:
        1. A base64 data URL (data:image/...;base64,...)
        2. A base64 string without prefix
        3. An HTTP(S) URL (store as-is)
        
        Returns:
            - ContentFile object for base64 images
            - URL string if already a URL
            - None if invalid
        """
        if not photo_data:
            return None
        
        # Check if it's already an HTTP(S) URL
        if isinstance(photo_data, str) and (photo_data.startswith('http://') or photo_data.startswith('https://')):
            # For URLs, we need to return them as a special wrapper or handle in views
            # For now, return as CloudinaryURL marker for special handling
            return ('url', photo_data)
        
        # Try to process as base64
        try:
            base64_str = photo_data
            
            # If it's a data URL, extract the base64 part
            if isinstance(photo_data, str) and photo_data.startswith('data:'):
                _, base64_str = photo_data.split(',', 1)
            
            # Decode base64
            decoded_data = base64.b64decode(base64_str)
            
            # Create a file with a unique name
            filename = f"property_photo_{uuid.uuid4()}.jpg"
            
            # Return ContentFile object with filename
            # The filename will be used when saving to storage
            return ContentFile(decoded_data, name=filename)
            
        except Exception as e:
            print(f"Error processing photo: {str(e)}")
            return None
    
    @staticmethod
    def get_photo_url(file_path):
        """
        Convert a stored file path to a full URL for response
        """
        if not file_path:
            return None
        
        # If it's already a full URL, return as-is
        if isinstance(file_path, str) and (file_path.startswith('http://') or file_path.startswith('https://')):
            return file_path
        
        # Otherwise, get the URL from storage
        try:
            return default_storage.url(file_path)
        except:
            return None
