from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('job/<int:pk>/', views.job_detail, name='job_detail'),
    path('job/<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('success/', views.application_success, name='application_success'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('employer/post-job/', views.post_job, name='post_job'),
    path('employer/applications/<int:pk>/', views.employer_applications, name='employer_applications'),
    path('employer/applications/<int:pk>/update/', views.update_application_status, name='update_application_status'),
]