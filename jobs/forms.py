from django import forms  # Import Django form tools
from django.contrib.auth.forms import UserCreationForm  # Import built-in registration form
from django.contrib.auth.models import User  # Import User model
from .models import Application, Job, Profile  # Import models

class ApplicationForm(forms.ModelForm):  # Form for job applications
    class Meta:
        model = Application  # Connect form to Application model
        fields = ['applicant_name', 'applicant_email', 'cover_letter', 'cv']  # Form fields

        widgets = {
            'applicant_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),  # Name input
            'applicant_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),  # Email input
            'cover_letter': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Tell us why you are the best candidate...'}),  # Cover letter textarea
            'cv': forms.FileInput(attrs={'class': 'form-control'}),  # CV upload field
        }

class RegisterForm(UserCreationForm):  # User registration form
    role = forms.ChoiceField(
        choices=[('jobseeker', 'Job Seeker'), ('employer', 'Employer')],  # Role options
        widget=forms.Select(attrs={'class': 'form-control'})  # Dropdown styling
    )

    class Meta:
        model = User  # Connect form to User model
        fields = ['username', 'password1', 'password2', 'role']  # Registration fields

    def __init__(self, *args, **kwargs):  # Customize form fields
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Choose a username'})  # Username styling
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Choose a password'})  # Password styling
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm your password'})  # Confirm password styling

class JobForm(forms.ModelForm):  # Form for posting jobs
    class Meta:
        model = Job  # Connect form to Job model
        fields = ['title', 'company', 'location', 'description']  # Job fields

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job title'}),  # Title input
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company name'}),  # Company input
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),  # Location input
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Job description'}),  # Description textarea
        }