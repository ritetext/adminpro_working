from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.db.models import Count, Avg
from board.models import Candidate, Exam, Question, Answer, Result
from .models import User

class CandidateInline(admin.StackedInline):
    model = Candidate
    can_delete = False
    verbose_name_plural = 'Candidate Profile'

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'full_name', 'is_admin', 
                   'is_candidate', 'phone_number', 'profile_image')
    list_filter = ('is_admin', 'is_candidate', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    ordering = ('username',)
    list_select_related = ['candidate']
    inlines = [CandidateInline]

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'profile_picture', 'phone_number')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_admin', 'is_candidate', 
                      'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'profile_picture', 'phone_number')
        }),
        ('Permissions', {
            'fields': ('is_admin', 'is_candidate')
        }),
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'

    def profile_image(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', 
                             obj.profile_picture.url)
        return "No Image"
    profile_image.short_description = 'Profile Picture'

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'user__email',
                   'exam_count', 'avg_score', 'last_exam_date')
    list_filter = ('user__is_active', 'user__date_joined')
    search_fields = ('user__username', 'user__email', 
                    'user__first_name', 'user__last_name')
    readonly_fields = ('exam_count', 'avg_score', 'last_exam_date')

    def exam_count(self, obj):
        return Result.objects.filter(candidate=obj).count()
    exam_count.short_description = 'Exams Taken'

    def avg_score(self, obj):
        avg = Result.objects.filter(candidate=obj).aggregate(Avg('score'))['score__avg']
        return f"{avg:.1f}%" if avg else "No exams"
    avg_score.short_description = 'Average Score'

    def last_exam_date(self, obj):
        last_result = Result.objects.filter(candidate=obj).order_by('-id').first()
        return last_result.created_at if last_result else "No exams"
    last_exam_date.short_description = 'Last Exam Date'

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    min_num = 2

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('exam', 'text', 'created_at', 'correct_answer', 'answer_count')
    list_filter = ('exam', 'created_at')
    search_fields = ('text', 'exam__title')
    inlines = [AnswerInline]

    def answer_count(self, obj):
        return obj.answers.count()
    answer_count.short_description = 'Total Answers'

    def correct_answer(self, obj):
        correct = obj.answers.filter(is_correct=True).first()
        return correct.text if correct else "No correct answer set"
    correct_answer.short_description = 'Correct Answer'

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'pass_mark', 'is_active', 
                   'question_count', 'total_attempts', 'pass_rate')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    actions = ['activate_exams', 'deactivate_exams']

    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Questions'

    def total_attempts(self, obj):
        return obj.result_set.count()
    total_attempts.short_description = 'Total Attempts'

    def pass_rate(self, obj):
        total = obj.result_set.count()
        if total:
            passed = obj.result_set.filter(is_passed=True).count()
            return f"{(passed/total)*100:.1f}%"
        return "No attempts"
    pass_rate.short_description = 'Pass Rate'

    @admin.action(description='Activate selected exams')
    def activate_exams(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} exams were activated.')

    @admin.action(description='Deactivate selected exams')
    def deactivate_exams(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} exams were deactivated.')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'exam', 'score', 'is_passed', 
                   'created_at', 'certificate_link')
    list_filter = ('is_passed', 'created_at', 'exam')
    search_fields = ('candidate__user__username', 'exam__title')
    readonly_fields = ('is_passed', 'created_at')

    def certificate_link(self, obj):
        if obj.is_passed:
            return format_html(
                '<a href="/generate-certificate/{}/" class="button" target="_blank">'
                'Download Certificate</a>', obj.id
            )
        return "Not Eligible"
    certificate_link.short_description = 'Certificate'

# Customize admin site
admin.site.site_header = 'Exam Administration'
admin.site.site_title = 'Exam Admin Portal'
admin.site.index_title = 'Welcome to Exam Administration'

# Answer Admin
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct')
    search_fields = ('text',)

