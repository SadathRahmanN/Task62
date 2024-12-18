from django.contrib import admin
from .models import User, Project

# Customize the User admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'bio', 'skills', 'contact')  # Fields to display in the admin list
    search_fields = ('username', 'email', 'skills')  # Fields for the search bar
    list_filter = ('is_active', 'is_staff', 'is_superuser')  # Add filters for the user status
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')  # Basic fields
        }),
        ('Personal Info', {
            'fields': ('bio', 'skills', 'contact')  # Custom fields added to the user model
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    ordering = ('username',)  # Default ordering by username


# Customize the Project admin
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'updated_at')  # Fields to display in the admin list
    search_fields = ('name', 'user__username', 'description')  # Fields for the search bar
    list_filter = ('created_at', 'updated_at')  # Filters for creation and update timestamps
    readonly_fields = ('created_at', 'updated_at')  # Make timestamps read-only
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'description')  # Essential fields
        }),
        ('Additional Info', {
            'fields': ('image_url', 'link', 'created_at', 'updated_at')  # Optional fields
        }),
    )
    ordering = ('-created_at',)  # Default ordering by the newest projects
