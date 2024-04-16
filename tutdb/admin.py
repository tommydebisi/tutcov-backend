from django.contrib import admin

# Register your models here.
from .models import User, Token, Department, Question

admin.site.register(User)

class TokenAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at", "access_token_expires_at"]
    list_filter = ["user"]


admin.site.register(Token, TokenAdmin)


class DepartmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Department, DepartmentAdmin)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question']
    list_filter = ['question']
    search_fields = ['question', 'question_number']
    list_editable = ['question_number']
