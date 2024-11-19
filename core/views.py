from django.shortcuts import render
from django.core.mail import send_mail, EmailMessage, BadHeaderError
from .task import notify_customer

# Create your views here.

def send_email(request):
    notify_customer.delay("This is a message from celery ")

    return render(request, 'hello.html', {'name': 'Mosh'})