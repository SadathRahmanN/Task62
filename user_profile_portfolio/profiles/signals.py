from django.db.backends.signals import connection_created
from django.db import connection
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, User

# Enable foreign key constraints for SQLite
def enable_foreign_keys(sender, connection, **kwargs):
    if connection.vendor == 'sqlite':
        with connection.cursor() as cursor:
            cursor.execute('PRAGMA foreign_keys = ON;')

# Connect the signal to the connection_created event
connection_created.connect(enable_foreign_keys)

# Signal to create a UserProfile when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a user profile when a new user is created."""
    if created:
        # Check if the user already has a profile; if not, create one
        if not hasattr(instance, 'profile'):
            UserProfile.objects.create(user=instance)
        else:
            instance.profile.save()

# Signal to save the user profile after a user is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the user profile whenever the user instance is saved."""
    try:
        # Ensure the user has a profile and save it
        if instance.profile:
            instance.profile.save()
    except UserProfile.DoesNotExist:
        # If the user doesn't have a profile, create it
        UserProfile.objects.create(user=instance)
