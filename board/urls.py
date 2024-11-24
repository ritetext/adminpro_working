from rest_framework_nested import routers
from django.urls import path, include
from . import views

# Main router
router = routers.DefaultRouter()
router.register('candidates', views.CandidateViewSet)
router.register('exams', views.ExamViewSet)
router.register('results', views.ResultViewSet, basename='result')
router.register('questions', views.QuestionViewSet, basename='question')  # Add this line

# Nested router for questions under exams
exams_router = routers.NestedDefaultRouter(router, 'exams', lookup='exam')
exams_router.register('questions', views.QuestionViewSet, basename='exam-questions')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(exams_router.urls)),
]