from django.contrib import admin
from .models import User, Profile, Department, Faculty


admin.site.register([Department, Faculty])

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_active', 'is_superuser']
    list_filter  = ['is_active']
    search_fields = ["username", "email"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_filter = ['user']

