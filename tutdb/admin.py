from django.contrib import admin

# Register your models here.
from .models import User, Course, Choice,Enrollment, UserResponse, Session, Question, Department
from authapp.models import Token

admin.site.register(Choice)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'enrolled_at']
    list_filter = ['enrolled_at', 'course', 'user']
    search_fields = ['enrolled_at', 'course', 'user']


@admin.register(UserResponse)
class UserResponseAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'session', 'is_correct', 'created_at']

    


class TokenAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at", "access_token_expires_at"]
    list_filter = ["user"]


admin.site.register(Token, TokenAdmin)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'code']
    list_editable = ['code', 'year']
    search_fields = ['name', 'year', 'code']
    list_filter = ['year']
    prepopulated_fields = {"slug": ("name",), "code_slug": ("code",)}


class DepartmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Department, DepartmentAdmin)

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("session",)}


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'question_number']
    list_filter = ['question_number']
    search_fields = ['question', 'question_number']
    list_editable = ['question_number']
