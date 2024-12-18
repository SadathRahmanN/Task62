from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User model
class User(AbstractUser):
    bio = models.TextField(blank=True, null=True, verbose_name="Biography")
    skills = models.TextField(blank=True, null=True, verbose_name="Skills (comma-separated)")
    contact = models.EmailField(blank=True, null=True, verbose_name="Contact Email")

    def __str__(self):
        return self.username

    def get_skills_list(self):
        """Return the skills as a list, split by commas."""
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []

# Project model
class Project(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name="User"
    )
    name = models.CharField(max_length=200, verbose_name="Project Name")
    description = models.TextField(verbose_name="Project Description")
    image_url = models.URLField(
        blank=True,
        null=True,
        default='',
        verbose_name="Image URL"
    )
    link = models.URLField(
        blank=True,
        null=True,
        default='',
        verbose_name="Project Link"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['-created_at']  # Newest projects first
