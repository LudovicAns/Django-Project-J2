from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path('', views.select_job, name='select_job'),
    path('job/<int:job_id>/', views.job_feedbacks, name='job_feedbacks'),
    path('job_title/<int:job_title_id>/', views.job_title_feedbacks, name='job_title_feedbacks'),
    path('add/', views.add_feedback, name='add_feedback'),
    path('job/<int:job_id>/average/', views.job_average_rating, name='job_average_rating'),
    path('job_title/<int:job_title_id>/average/', views.job_title_average_rating, name='job_title_average_rating'),
]
