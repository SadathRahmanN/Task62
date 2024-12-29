from django.contrib import admin
from .models import User, Project

class ProjectInline(admin.TabularInline):
    model = Project
    extra = 1  # Add one extra form to add projects directly within the User admin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'bio', 'skills', 'contact')
    search_fields = ('username', 'email', 'skills', 'bio')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal Info', {
            'fields': ('bio', 'skills', 'contact')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    inlines = [ProjectInline]
    ordering = ('username',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'updated_at')
    search_fields = ('name', 'user__username', 'description')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at', 'user')  # Make user field read-only
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'description')
        }),
        ('Additional Info', {
            'fields': ('image_url', 'link', 'created_at', 'updated_at')
        }),
    )
    date_hierarchy = 'created_at'  # Adds date navigation
    ordering = ('-created_at',)
