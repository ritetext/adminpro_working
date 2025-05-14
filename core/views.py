from django.shortcuts import render
from django.core.mail import send_mail, EmailMessage, BadHeaderError
from .task import notify_customer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from adminpro.api_docs import email_send_schema

# Create your views here.

@swagger_auto_schema(method='post', **email_send_schema)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_email(request):
    """
    Send an email notification.
    """
    if request.method == 'POST':
        to = request.data.get('to')
        subject = request.data.get('subject')
        body = request.data.get('body')
        
        if not all([to, subject, body]):
            return Response({'error': 'Missing required fields'}, status=400)
        
        try:
            # Queue the email task
            notify_customer.delay(body)
            return Response({'status': 'Email queued successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    return Response({'error': 'Method not allowed'}, status=405)