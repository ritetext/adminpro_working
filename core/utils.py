from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF to provide consistent error responses.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # If the exception is not handled by DRF, handle it ourselves
    if response is None:
        return Response({
            'error': str(exc),
            'status_code': 500
        }, status=500)
    
    # If the response has data with a detail field, reformat it to our standard error format
    if isinstance(response.data, dict) and 'detail' in response.data:
        response.data = {
            'error': response.data['detail'],
            'status_code': response.status_code
        }
    
    return response 