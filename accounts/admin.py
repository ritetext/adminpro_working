from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from board.models import Candidate, Exam, Question, Answer, Result, generate_certificate
from .models import User

# Custom User Admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_admin', 'is_candidate', 'phone_number')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('username',)
    list_select_related = ['candidate']

    # Define the fields to be displayed in the admin user detail view
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),  # Ensure proper handling of password
        ('Personal Info', {'fields': ('first_name', 'last_name', 'profile_picture', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin', 'is_candidate', 'groups', 'user_permissions')}),
    )
    
    # Define the fields to be displayed when creating a new user
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password1', 'password2')}),  # Ensure password fields are handled properly
        ('Personal Info', {'fields': ('first_name', 'last_name', 'profile_picture', 'phone_number')}),
        ('Permissions', {'fields': ('is_admin', 'is_candidate')}),
    )

# Candidate Admin
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('user','first_name', 'last_name')
    search_fields = ('user__username', 'user__email')

# Exam Admin
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'pass_mark', 'is_active')
    search_fields = ('title',)

# Question Admin
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('exam', 'text', 'created_at')
    search_fields = ('text',)

# Answer Admin
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct')
    search_fields = ('text',)

# Result Admin
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'exam', 'score', 'is_passed')
    search_fields = ('candidate__user__username', 'exam__title')

# # Certificate admin
# @admin.register(generate_certificate)
# class CertificateAdmin(admin.ModelAdmin):
#     list_display = ('candidate', 'exam', 'issued_at')
#     search_fields = ('candidate__user__username', 'exam__title')