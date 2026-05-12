from django.shortcuts import render, get_object_or_404, redirect  # Import template rendering, object fetching, and page redirect functions
from django.contrib.auth import login, logout as auth_logout  # Import login and logout functions
from django.contrib.auth.decorators import login_required  # Import decorator to restrict access to logged-in users
from .models import Job, Application, Profile  # Import database models
from .forms import ApplicationForm, RegisterForm, JobForm  # Import forms

def job_list(request):  # Display all jobs
    jobs = Job.objects.all().order_by('-created_at')  # Get jobs ordered newest first
    query = request.GET.get('q')  # Get search keyword
    location = request.GET.get('location')  # Get location filter

    if query:
        jobs = jobs.filter(title__icontains=query) | jobs.filter(company__icontains=query)  # Filter by title or company

    if location:
        jobs = jobs.filter(location__icontains=location)  # Filter by location

    return render(request, 'jobs/job_list.html', {'jobs': jobs, 'query': query, 'location': location})  # Render job list page

def job_detail(request, pk):  # Show single job details
    job = get_object_or_404(Job, pk=pk)  # Fetch job or show 404
    return render(request, 'jobs/job_detail.html', {'job': job})  # Render detail page

@login_required  # Require login
def apply_job(request, pk):  # Handle job application
    job = get_object_or_404(Job, pk=pk)  # Get selected job

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)  # Load submitted form

        if form.is_valid():
            application = form.save(commit=False)  # Create application without saving
            application.job = job  # Attach job
            application.user = request.user  # Attach user
            application.save()  # Save application
            return redirect('application_success')  # Redirect after success
    else:
        form = ApplicationForm()  # Empty form

    return render(request, 'jobs/apply.html', {'form': form, 'job': job})  # Render application page

def application_success(request):  # Show success page
    return render(request, 'jobs/success.html')

def register(request):  # Handle user registration
    if request.method == 'POST':
        form = RegisterForm(request.POST)  # Load submitted data

        if form.is_valid():
            user = form.save()  # Save user
            role = form.cleaned_data.get('role')  # Get selected role
            Profile.objects.create(user=user, role=role)  # Create profile
            login(request, user)  # Log user in
            return redirect('job_list')  # Redirect to homepage
    else:
        form = RegisterForm()  # Empty form

    return render(request, 'jobs/register.html', {'form': form})  # Render registration page

def logout_view(request):  # Handle logout
    auth_logout(request)  # Log user out
    return redirect('job_list')  # Redirect homepage

@login_required
def my_applications(request):  # Show user's applications
    applications = Application.objects.filter(user=request.user).order_by('-applied_at')  # Get applications
    return render(request, 'jobs/my_applications.html', {'applications': applications})  # Render applications page

@login_required
def employer_dashboard(request):  # Employer dashboard
    try:
        profile = Profile.objects.get(user=request.user)  # Get user profile

        if profile.role != 'employer':
            return redirect('job_list')  # Redirect if not employer

    except Profile.DoesNotExist:
        return redirect('job_list')  # Redirect if profile missing

    jobs = Job.objects.filter(posted_by=request.user).order_by('-created_at')  # Get employer jobs
    return render(request, 'jobs/employer_dashboard.html', {'jobs': jobs})  # Render dashboard

@login_required
def post_job(request):  # Handle job posting
    try:
        profile = Profile.objects.get(user=request.user)  # Get profile

        if profile.role != 'employer':
            return redirect('job_list')  # Redirect if not employer

    except Profile.DoesNotExist:
        return redirect('job_list')

    if request.method == 'POST':
        form = JobForm(request.POST)  # Load submitted job form

        if form.is_valid():
            job = form.save(commit=False)  # Create job without saving
            job.posted_by = request.user  # Attach employer
            job.save()  # Save job
            return redirect('employer_dashboard')  # Redirect dashboard
    else:
        form = JobForm()  # Empty form

    return render(request, 'jobs/post_job.html', {'form': form})  # Render post job page

@login_required
def employer_applications(request, pk):  # Show applications for a job
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)  # Get employer's job
    applications = Application.objects.filter(job=job).order_by('-applied_at')  # Get applications
    return render(request, 'jobs/employer_applications.html', {'job': job, 'applications': applications})  # Render page

@login_required
def update_application_status(request, pk):  # Update application status
    application = get_object_or_404(Application, pk=pk)  # Get application

    if request.method == 'POST':
        status = request.POST.get('status')  # Get new status
        application.status = status  # Update status
        application.save()  # Save changes

    return redirect('employer_applications', pk=application.job.pk)  # Redirect back