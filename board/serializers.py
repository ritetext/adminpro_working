from rest_framework import serializers
from board.models import Answer, Question, Exam, Candidate, Result, CandidateImage



class QuestionSerializer(serializers.ModelSerializer):
    exam = serializers.PrimaryKeyRelatedField(queryset=Exam.objects.all())

    class Meta:
        model = Question
        fields = ['id', 'exam', 'text', 'created_at']

class AnswerSerializer(serializers.ModelSerializer):
    #question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())

    class Meta:
        model = Answer
        fields = ['question', 'text', 'is_correct']

class ExamSerializers(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['title', 'duration','pass_mark', 'is_active']


class CandidateImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        candidate_id = self.context['candidate_id']
        return CandidateImage.objects.create(candidate_id=candidate_id, **validated_data)

    class Meta:
        model = CandidateImage
        fields = ['id', 'image']

class CandidateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    images = CandidateImageSerializer(many=True, read_only=True)
    class Meta:
        model = Candidate
        fields = ['user_id', 'phone', 'images']

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model=Result
        fields = ['candidate', 'exam', 'score', 'is_passed']


