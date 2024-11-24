from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from board.models import Candidate, Exam, Question, Answer, Result, CandidateImage

User = get_user_model()

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 
                 'last_name', 'phone_number', 'is_candidate']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                 'phone_number', 'is_candidate']

class CandidateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Candidate
        fields = ['id', 'user', 'first_name', 'last_name', 'phone', 'email']

# Add this new serializer to your serializers.py
class CandidateImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateImage
        fields = ['id', 'candidate', 'image', 'is_primary']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']

    def to_representation(self, instance):
        """Hide is_correct field from non-staff users"""
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if request and not request.user.is_staff:
            ret.pop('is_correct', None)
        return ret

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'answers', 'created_at']

class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'duration', 'pass_mark', 'is_active', 'questions']

    def to_representation(self, instance):
        """Show questions only in detail view"""
        ret = super().to_representation(instance)
        if not self.context.get('detail', False):
            ret.pop('questions', None)
        return ret

class ExamSubmissionSerializer(serializers.Serializer):
    answers = serializers.DictField(
        child=serializers.IntegerField(),
        help_text="Dictionary of question_id: answer_id pairs"
    )

    def validate_answers(self, value):
        exam_id = self.context.get('exam_id')
        if not exam_id:
            raise serializers.ValidationError("Exam ID is required")

        questions = Question.objects.filter(exam_id=exam_id)
        question_ids = set(questions.values_list('id', flat=True))
        submitted_ids = set(int(k) for k in value.keys())

        if submitted_ids != question_ids:
            raise serializers.ValidationError("All questions must be answered")

        for question_id, answer_id in value.items():
            if not Answer.objects.filter(
                question_id=question_id, 
                id=answer_id
            ).exists():
                raise serializers.ValidationError(
                    f"Invalid answer for question {question_id}"
                )
        return value

class ResultSerializer(serializers.ModelSerializer):
    candidate_name = serializers.SerializerMethodField()
    exam_title = serializers.CharField(source='exam.title', read_only=True)

    class Meta:
        model = Result
        fields = ['id', 'candidate', 'candidate_name', 'exam', 
                 'exam_title', 'score', 'is_passed']
        read_only_fields = ['score', 'is_passed']

    def get_candidate_name(self, obj):
        return f"{obj.candidate.user.first_name} {obj.candidate.user.last_name}"