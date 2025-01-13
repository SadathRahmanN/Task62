from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

# Custom User model
class User(AbstractUser):
    bio = models.TextField(blank=True, null=True, verbose_name="Biography")
    skills = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Skills (comma-separated)"
    )
    contact = models.EmailField(
        blank=True, 
        null=True, 
        verbose_name="Contact Email"
    )
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        blank=True,
        null=True,
        verbose_name="Profile Photo"
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    def __str__(self):
        return self.username

    def get_skills_list(self):
        """Return the skills as a list, split by commas."""
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


# Project model
class Project(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='projects',
        verbose_name="User",
        null=True
    )
    name = models.CharField(max_length=200, verbose_name="Project Name")
    description = models.TextField(verbose_name="Project Description")
    image_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Image URL"
    )
    link = models.URLField(
        blank=True,
        null=True,
        verbose_name="Project Link"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    project_image = models.ImageField(
        upload_to='project_images/',
        blank=True,
        null=True,
        verbose_name="Project Image"
    )

    category = models.CharField(max_length=100, blank=True, null=True, verbose_name="Category")

    status = models.CharField(
        max_length=10, 
        choices=[('active', 'Active'), ('completed', 'Completed'), ('archived', 'Archived')],
        default='active', 
        verbose_name="Project Status"
    )

    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name="Slug")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['-created_at']


# ContactRequest model
class ContactRequest(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='contact_requests',
        verbose_name="User"
    )
    message = models.TextField(verbose_name="Message")
    email = models.EmailField(verbose_name="Contact Email")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f"Contact Request from {self.email}"

    class Meta:
        verbose_name = "Contact Request"
        verbose_name_plural = "Contact Requests"


# UserProfile model
class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="User"
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Phone Number")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Date of Birth")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


# UserActivity model
class UserActivity(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='activities',
        verbose_name="User"
    )
    action = models.CharField(max_length=255, verbose_name="Action Performed")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Action Timestamp")
    details = models.TextField(blank=True, null=True, verbose_name="Details")

    def __str__(self):
        return f"{self.user.username} performed {self.action} on {self.timestamp}"

    class Meta:
        verbose_name = "User Activity"
        verbose_name_plural = "User Activities"


# Follow model
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"

    class Meta:
        verbose_name = "Follow"
        verbose_name_plural = "Follows"
