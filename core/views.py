from django.shortcuts import render
from django.core.mail import send_mail, EmailMessage, BadHeaderError

# Create your views here.

def send_email(request):
    try:
        send_mail('subject', 'message', 'admin@techternet.com',
              ['user@techternet.com'])
    except BadHeaderError:
        pass

    return render(request, 'hello.html', {'name': 'Mosh'})