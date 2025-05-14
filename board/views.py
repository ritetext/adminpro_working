from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from .models import (
    Candidate, CandidateImage, Exam, Question, Answer, Result)
from .serializers import ( CandidateSerializer, CandidateImageSerializer,
    ExamSerializer, QuestionSerializer, ResultSerializer, ExamSubmissionSerializer
)
from .permissions import IsAdminUser, IsStudentUser, IsOwnerOrAdmin
from drf_yasg.utils import swagger_auto_schema
from adminpro.api_docs import (
    candidate_list_schema, candidate_create_schema, candidate_retrieve_schema,
    exam_list_schema, exam_retrieve_schema, exam_submit_schema,
    result_list_schema, result_retrieve_schema,
    question_list_schema, question_create_schema
)

class CandidateViewSet(mixins.CreateModelMixin, 
                       mixins.UpdateModelMixin, 
                       mixins.RetrieveModelMixin, 
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """
    ViewSet for managing candidates.
    Provides CRUD operations and image listing.
    """
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    
    @swagger_auto_schema(**candidate_list_schema)
    def list(self, request):
        """List candidates based on permissions"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(**candidate_retrieve_schema)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(**candidate_create_schema)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        method='get',
        operation_summary="Current User's Candidate Profile",
        operation_description="Get the current user's candidate profile"
    )
    @swagger_auto_schema(
        method='put',
        operation_summary="Update Current User's Candidate Profile",
        operation_description="Update the current user's candidate profile"
    )
    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        # Use get to retrieve the candidate for the logged-in user
        try:
            candidate = Candidate.objects.get(user_id=request.user.id)
        except Candidate.DoesNotExist:
            return Response({"detail": "Candidate not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = CandidateSerializer(candidate)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CandidateSerializer(candidate, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # Return empty queryset for Swagger schema generation
            return Candidate.objects.none()
            
        if self.request.user.is_staff and not self.request.user.is_candidate:
            return Candidate.objects.all()
        return Candidate.objects.filter(user=self.request.user)
    
    @swagger_auto_schema(
        operation_summary="List Candidate Images",
        operation_description="List all images for a specific candidate"
    )
    @action(detail=True)
    def images(self, request, pk=None):
        """List all images for a specific candidate."""
        candidate = self.get_object()
        images = CandidateImage.objects.filter(candidate=candidate)
        serializer = CandidateImageSerializer(images, many=True)
        return Response(serializer.data)

class CandidateImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing candidate images.
    Supports file upload and basic CRUD operations.
    """
    serializer_class = CandidateImageSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        return CandidateImage.objects.filter(
            candidate_id=self.kwargs['candidate_pk']
        )

    def perform_create(self, serializer):
        candidate = get_object_or_404(
            Candidate, 
            id=self.kwargs['candidate_pk']
        )
        if not self.request.user.is_staff and candidate.user != self.request.user:
            raise PermissionDenied(
                "You don't have permission to add images for this candidate"
            )
        serializer.save(candidate=candidate)

class ExamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing exams.
    Provides CRUD operations and exam submission functionality.
    """
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**exam_list_schema)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(**exam_retrieve_schema)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['detail'] = self.action == 'retrieve'
        return context

    @swagger_auto_schema(**exam_submit_schema)
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Handle exam submission and calculate results."""
        exam = self.get_object()
        if not exam.is_active:
            return Response(
                {"error": "This exam is not active"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ExamSubmissionSerializer(
            data=request.data,
            context={'exam_id': exam.id}
        )

        if serializer.is_valid():
            candidate = get_object_or_404(Candidate, user=request.user)
            
            # Prevent multiple attempts
            if Result.objects.filter(candidate=candidate, exam=exam).exists():
                return Response(
                    {"error": "You have already attempted this exam"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Process answers and calculate score
            result = self._process_exam_submission(
                candidate, 
                exam, 
                serializer.validated_data['answers']
            )
            
            return Response(ResultSerializer(result).data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def _process_exam_submission(self, candidate, exam, answers):
        """Helper method to process exam submission and calculate score."""
        correct_answers = sum(
            1 for question_id, answer_id in answers.items()
            if Answer.objects.filter(
                question_id=question_id,
                id=answer_id,
                is_correct=True
            ).exists()
        )

        total_questions = exam.questions.count()
        score = (correct_answers / total_questions) * 100
        is_passed = score >= exam.pass_mark

        return Result.objects.create(
            candidate=candidate,
            exam=exam,
            score=score,
            is_passed=is_passed
        )

class QuestionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing exam questions.
    Provides CRUD operations for questions.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(**question_list_schema)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(**question_create_schema)
    def create(self, request, *args, **kwargs):
        # Add better error handling
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            # Log the error for debugging
            print(f"Question creation error: {str(e)}")
            return Response(
                {"error": f"Failed to create question: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # Return empty queryset for Swagger schema generation
            return Question.objects.none()
            
        if 'exam_pk' in self.kwargs:
            return Question.objects.filter(exam_id=self.kwargs['exam_pk'])
        return Question.objects.all()
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

class ResultViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing exam results.
    Provides read-only access to results.
    """
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    
    @swagger_auto_schema(**result_list_schema)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(**result_retrieve_schema)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # Return empty queryset for Swagger schema generation
            return Result.objects.none()
            
        # Admin users can see all results
        if self.request.user.is_staff:
            return Result.objects.all().select_related('candidate', 'exam')
        
        # Regular users can only see their own results
        try:
            candidate = Candidate.objects.get(user=self.request.user)
            return Result.objects.filter(candidate=candidate).select_related('candidate', 'exam')
        except Candidate.DoesNotExist:
            return Result.objects.none()