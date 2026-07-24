import base64
import uuid
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

MIME_EXTENSION_MAP = {
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/png": "png",
    "image/gif": "gif",
    "image/webp": "webp",
    "application/pdf": "pdf",
}

IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}


class ImageUtils:
    """Utility class for handling image uploads and base64 conversions"""

    @staticmethod
    def _sniff_extension(decoded_data: bytes) -> str:
        """Best-effort file type detection from magic bytes, used when no mime type is given."""
        if decoded_data.startswith(b"\xff\xd8\xff"):
            return "jpg"
        if decoded_data.startswith(b"\x89PNG\r\n\x1a\n"):
            return "png"
        if decoded_data.startswith((b"GIF87a", b"GIF89a")):
            return "gif"
        if decoded_data.startswith(b"%PDF"):
            return "pdf"
        if decoded_data.startswith(b"RIFF") and decoded_data[8:12] == b"WEBP":
            return "webp"
        return "jpg"

    @staticmethod
    def is_image_extension(extension: str) -> bool:
        return (extension or "").lower().lstrip(".") in IMAGE_EXTENSIONS

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
            mime_type = None

            # If it's a data URL, extract the mime type and the base64 part
            if isinstance(photo_data, str) and photo_data.startswith('data:'):
                header, base64_str = photo_data.split(',', 1)
                mime_type = header[len('data:'):].split(';')[0] or None

            # Decode base64
            decoded_data = base64.b64decode(base64_str)

            # Determine the real file extension instead of assuming .jpg
            extension = MIME_EXTENSION_MAP.get(mime_type) if mime_type else None
            if not extension:
                extension = ImageUtils._sniff_extension(decoded_data)

            # Create a file with a unique name
            filename = f"property_photo_{uuid.uuid4()}.{extension}"

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
