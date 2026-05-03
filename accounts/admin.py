from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_organizer_requested', 'is_staff')
    list_filter = ('role', 'is_organizer_requested')
    fieldsets = UserAdmin.fieldsets + (
        ('Status Tracking', {'fields': ('role', 'is_organizer_requested')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)