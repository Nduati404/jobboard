from django.db import models # Imports Django models
from django.contrib.auth.models import User # Imports Django User model

class Job(models.Model): # Model for job posts
    title = models.CharField(max_length=200) # Job title
    company = models.CharField(max_length=200) # Company name
    location = models.CharField(max_length=200) # Job location
    description = models.TextField() # Job details
    created_at = models.DateTimeField(auto_now_add=True) # Date created
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # User who posted the job

    def __str__(self): # Shows object as text
        return self.title # Displays job title


class Application(models.Model): # Model for job applications
    STATUS_CHOICES = [
        ('pending', 'Pending'), # Waiting
        ('accepted', 'Accepted'), # Approved
        ('rejected', 'Rejected'), # Denied
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE) # Linked job
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Linked user
    applicant_name = models.CharField(max_length=200) # Applicant name
    applicant_email = models.EmailField() # Applicant email
    cover_letter = models.TextField() # Cover letter
    cv = models.FileField(upload_to='cvs/') # Uploaded CV
    applied_at = models.DateTimeField(auto_now_add=True) # Application date
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending') # Application status

    def __str__(self): # Shows object as text
        return f"{self.applicant_name} - {self.status}" # Applicant and status


class Profile(models.Model): # Extra user information
    ROLE_CHOICES = [
        ('jobseeker', 'Job Seeker'), # Looking for jobs
        ('employer', 'Employer'), # Posting jobs
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE) # One profile per user
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='jobseeker') # User role

    def __str__(self): # Shows object as text
        return f"{self.user.username} - {self.role}" # Username and role