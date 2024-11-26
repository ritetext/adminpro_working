from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.contrib import admin
from board.validators import vaidate_file_size

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    'created_at' and 'modified_at' fields.
    """
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True

class Candidate(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='candidate_profile'
    )
    phone = models.CharField(max_length=20)
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        indexes = [
            models.Index(fields=['phone']),
        ]

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    def get_full_name(self):
        return f'{self.first_name()} {self.last_name()}'

class CandidateImage(TimeStampedModel):
    """
    Model for storing candidate profile images.
    """
    candidate = models.ForeignKey(
        Candidate, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(
        upload_to='store/images/%Y/%m',
        validators=[vaidate_file_size]
    )
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_primary', '-created_at']

class Exam(TimeStampedModel):
    """
    Model representing an examination.
    """
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration = models.DurationField(help_text="Duration in minutes")
    pass_mark = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    is_active = models.BooleanField(default=True)
    total_questions = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active', '-created_at']),
        ]

    def __str__(self):
        return self.title
    
    def update_total_questions(self):
        self.total_questions = self.questions.count()
        self.save()

class Question(TimeStampedModel):
    """
    Model representing exam questions.
    """
    exam = models.ForeignKey(
        Exam, 
        related_name='questions', 
        on_delete=models.CASCADE
    )
    text = models.TextField()
    marks = models.PositiveIntegerField(default=1)
    explanation = models.TextField(blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.text
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.exam.update_total_questions()

class Answer(TimeStampedModel):
    """
    Model representing answers to questions.
    """
    question = models.ForeignKey(
        Question, 
        related_name='answers', 
        on_delete=models.CASCADE
    )
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.text

class Result(TimeStampedModel):
    """
    Model representing exam results.
    """
    candidate = models.ForeignKey(
        Candidate, 
        on_delete=models.CASCADE,
        related_name='exam_results'
    )
    exam = models.ForeignKey(
        Exam, 
        on_delete=models.CASCADE,
        related_name='results'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    is_passed = models.BooleanField()
    completed_at = models.DateTimeField(default=timezone.now)
    certificate_path = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-completed_at']
        unique_together = ['candidate', 'exam']
        indexes = [
            models.Index(fields=['candidate', 'exam']),
            models.Index(fields=['is_passed', '-completed_at']),
        ]

    def save(self, *args, **kwargs):
        self.is_passed = self.score >= self.exam.pass_mark
        if self.is_passed and not self.certificate_path:
            self.certificate_path = self.generate_certificate()
        super().save(*args, **kwargs)

    def generate_certificate(self):
        """Generate PDF certificate for passed exams"""
        file_name = f"{self.candidate.get_full_name()}_{self.exam.title}_{timezone.now().strftime('%Y%m%d')}.pdf"
        file_path = f"certificates/{file_name}"
        full_path = f"media/{file_path}"
        
        c = canvas.Canvas(full_path, pagesize=A4)
        c.drawString(100, 750, "Certificate of Completion")
        c.drawString(100, 700, 
            f"This certifies that {self.candidate.get_full_name()} "
            f"has passed the {self.exam.title} exam with {self.score}%.")
        c.drawString(100, 650, 
            f"Completed on: {self.completed_at.strftime('%B %d, %Y')}")
        c.save()
        
        return file_path