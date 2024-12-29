from django import forms
from .models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['bio', 'skills', 'contact', 'profile_photo']  # Added 'profile_photo'
        widgets = {
            'bio': forms.Textarea(attrs={'placeholder': 'Write about yourself...', 'rows': 4}),
            'skills': forms.Textarea(attrs={'placeholder': 'E.g., Python, Django, HTML, CSS', 'rows': 3}),
            'contact': forms.EmailInput(attrs={'placeholder': 'example@email.com'}),
        }
