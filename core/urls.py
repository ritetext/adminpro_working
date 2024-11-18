from django.urls import path
from core import views

urlpatterns = [
    path('mails/', views.send_email)
]