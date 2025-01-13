from django import forms
from .models import User, Project

# Profile Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['bio', 'skills', 'contact', 'profile_photo']  # Includes 'profile_photo'
        widgets = {
            'bio': forms.Textarea(attrs={
                'placeholder': 'Write about yourself...',
                'rows': 4,
                'class': 'form-control',
            }),
            'skills': forms.Textarea(attrs={
                'placeholder': 'E.g., Python, Django, HTML, CSS',
                'rows': 3,
                'class': 'form-control',
            }),
            'contact': forms.EmailInput(attrs={
                'placeholder': 'example@email.com',
                'class': 'form-control',
            }),
            'profile_photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

# Project Form
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'image_url', 'link']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Project Name',
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe your project...',
                'rows': 4,
                'class': 'form-control',
            }),
            'image_url': forms.URLInput(attrs={
                'placeholder': 'Image URL (optional)',
                'class': 'form-control',
            }),
            'link': forms.URLInput(attrs={
                'placeholder': 'Project Link (e.g., GitHub, live site)',
                'class': 'form-control',
            }),
        }

# User Signup Form
class UserSignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'form-control',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Choose a username',
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your email address',
                'class': 'form-control',
            }),
        }
