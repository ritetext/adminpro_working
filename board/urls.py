from django.urls import path
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('questions', views.QuestionViewSet)
router.register('answers', views.AnswerViewSet)
router.register('exams', views.ExamViewSet)
router.register('candidates', views.CandidateViewSet)
router.register('result', views.ResultViewSet)



questions_router = routers.NestedDefaultRouter(router, 'questions', lookup='question')
questions_router.register('answers', views.AnswerViewSet, basename='question-answers')

# Nested Router for 'candidates' (added 'images')
candidate_router = routers.NestedDefaultRouter(
    router, 'candidates', lookup='candidate')
candidate_router.register(
    'images', views.CandidateImageViewSet, basename='candidate-image')

# Combine all URL patterns
urlpatterns = router.urls + questions_router.urls + candidate_router.urls
#URLConf
#urlpatterns = [""" 
 #   path('questions/', views.QuestionList.as_view()),
  #  path('questions/<int:id>/', views.QuestionDetail.as_view()) """
#]