from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.contrib import admin
from board.validators import vaidate_file_size

# Candidate model
class Candidate(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    def last_name(self):
        return self.user.last_name

class CandidateImage(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='store/images', validators=[vaidate_file_size])


# Exam model
class Exam(models.Model):
    title = models.CharField(max_length=100)
    duration = models.TimeField()
    pass_mark = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# Question model
class Question(models.Model):
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

# Answer model
class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
# Result model
class Result(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.IntegerField()
    is_passed = models.BooleanField()

# Function to generate PDF certificate
def generate_certificate(candidate_name, exam_title):
    file_path = f"media/certificates/{candidate_name}_certificate.pdf"
    c = canvas.Canvas(file_path, pagesize=A4)
    c.drawString(100, 750, f"Certificate of Completion")
    c.drawString(100, 700, f"This certifies that {candidate_name} has passed the {exam_title} exam.")
    c.save()
    return file_path