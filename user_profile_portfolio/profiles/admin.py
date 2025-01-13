from django.contrib import admin
from .models import User, Project

# Inline class to add Projects directly within the User admin interface
class ProjectInline(admin.TabularInline):
    model = Project
    extra = 1  # Allows adding one extra project inline
    fields = ('name', 'description', 'image_url', 'link')  # Specify the fields to show
    verbose_name = "Project"
    verbose_name_plural = "Projects"

# Custom admin for User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'bio', 'get_skills', 'contact', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'skills', 'bio')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    ordering = ('username',)
    inlines = [ProjectInline]

    # Custom method to display skills as a comma-separated string
    def get_skills(self, obj):
        return ', '.join(obj.get_skills_list())
    get_skills.short_description = "Skills"

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password', 'profile_photo')
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

# Custom admin for Project
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'updated_at', 'project_image_display')
    search_fields = ('name', 'user__username', 'description')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')  # Ensure created_at and updated_at are read-only
    date_hierarchy = 'created_at'

    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'description')
        }),
        ('Additional Info', {
            'fields': ('image_url', 'link', 'project_image', 'created_at', 'updated_at')
        }),
    )

    # Custom method to display the project image in admin list
    def project_image_display(self, obj):
        if obj.project_image:
            return f"Yes ({obj.project_image.name})"
        return "No"
    project_image_display.short_description = "Has Image"

# Register the User and Project admin configurations
admin.site.site_header = "Project Management Admin"
admin.site.site_title = "Project Management Admin Portal"
admin.site.index_title = "Welcome to the Project Management Admin"
