from drf_spectacular.utils import OpenApiResponse, OpenApiParameter

class SwaggerPage:
    
    @staticmethod
    def response(description="Success", response=None):
        return {200: OpenApiResponse(description=description, response=response)}
    
    @staticmethod
    def get_all_parameters():
        return [
            OpenApiParameter(name="page", description="Page number", required=False, type=int),
            OpenApiParameter(name="size", description="Page size", required=False, type=int),
            OpenApiParameter(name="search", description="Search term", required=False, type=str)
        ]
    
    @staticmethod
    def search_parameters(key_description):
        return [
            OpenApiParameter(name="query", description=key_description, required=True, type=str)
        ]
