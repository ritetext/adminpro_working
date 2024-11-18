from rest_framework.decorators import api_view, action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import QuestionFilter
from .models import Question, Answer, Exam, Candidate, Result, CandidateImage
from .permissions import IsAdminOrReadOnly
from .serializers import CandidateImageSerializer, QuestionSerializer, AnswerSerializer, ExamSerializers, CandidateSerializer, ResultSerializer


class QuestionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = QuestionFilter  # Updated to `filterset_class`
    search_fields = ['text']
    pagination_class = PageNumberPagination


class AnswerViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class ExamViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Exam.objects.all()
    serializer_class = ExamSerializers


class CandidateViewSet(ModelViewSet):
    # Only admin users can access by default
    #permission_classes = [IsAdminUser]
    queryset = Candidate.objects.prefetch_related('images').all()
    serializer_class = CandidateSerializer

    @action(detail=False, methods=['get', 'put'], permission_classes=[IsAuthenticated])
    def me(self, request):
        candidate, created = Candidate.objects.get_or_create(
            user_id=request.user.id)
        if request.method == "GET":
            serializer = CandidateSerializer(candidate)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = CandidateSerializer(candidate, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class ResultViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

class CandidateImageViewSet(ModelViewSet):
    serializer_class = CandidateImageSerializer
    #queryset = CandidateImage.objects.all()

    def get_serializer_context(self):
        return {'candidate_id': self.kwargs['candidate_pk']}

    #Get a single image
    def get_queryset(self):
        return CandidateImage.objects.filter(candidate_id=self.kwargs['candidate_pk'])
