import json
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class APIErrorMiddleware(MiddlewareMixin):
    """
    Middleware to handle API errors and provide consistent error responses.
    """
    def process_exception(self, request, exception):
        if request.path.startswith('/api/'):
            # Only handle exceptions for API endpoints
            data = {
                'error': str(exception),
                'status_code': 500
            }
            return JsonResponse(data, status=500)
        return None 