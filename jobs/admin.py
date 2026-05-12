from django.contrib import admin
from django.core.mail import send_mail
from .models import Job, Application

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'created_at']
    search_fields = ['title', 'company', 'location']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant_name', 'applicant_email', 'job', 'status', 'applied_at']
    list_filter = ['status']
    search_fields = ['applicant_name', 'applicant_email']

    def save_model(self, request, obj, form, change):
        print("SAVE MODEL CALLED")
        print(f"Change: {change}")
        if change:
            try:
                old_obj = Application.objects.get(pk=obj.pk)
                print(f"Old status: {old_obj.status}, New status: {obj.status}")
                if old_obj.status != obj.status:
                    print("STATUS CHANGED - Sending email...")
                    if obj.status == 'accepted':
                        subject = f'Congratulations! Your application for {obj.job.title} has been Accepted'
                        message = f'Dear {obj.applicant_name}, your application has been ACCEPTED!'
                    elif obj.status == 'rejected':
                        subject = f'Update on your application for {obj.job.title}'
                        message = f'Dear {obj.applicant_name}, your application was not successful.'
                    else:
                        subject = None

                    if subject:
                        send_mail(
                            subject,
                            message,
                            'jobboard@gmail.com',
                            [obj.applicant_email],
                            fail_silently=False,
                        )
                        print("EMAIL SENT!")
            except Exception as e:
                print(f"ERROR: {e}")
        super().save_model(request, obj, form, change)