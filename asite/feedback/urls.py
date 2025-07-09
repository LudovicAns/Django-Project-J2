from django.urls import path
from . import views

urlpatterns = [
    path('', views.select_job, name='select_job'),
    path('job/<int:job_id>/', views.job_feedbacks, name='job_feedbacks'),
    path('add/', views.add_feedback, name='add_feedback'),
    path('job/<int:job_id>/average/', views.job_average_rating, name='job_average_rating'),
]
