from django.contrib import admin

# Register your models here.
from .models import User, Course, Token, Department, Question

admin.site.register(User)

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


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'question_number', 'session']
    list_filter = ['question']
    search_fields = ['question', 'question_number']
    list_editable = ['question_number']
