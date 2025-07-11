from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView

from . import views

# API router for JobRecord
jobs_router = DefaultRouter()
jobs_router.register('jobs', views.JobRecordViewSet)

# API router for related entities
entities_router = DefaultRouter()
entities_router.register('category', views.CategoryViewSet)
entities_router.register('contract', views.ContractViewSet)
entities_router.register('skill', views.SkillViewSet)
entities_router.register('industry', views.IndustryViewSet)
entities_router.register('job-title', views.JobTitleViewSet)
entities_router.register('location', views.LocationViewSet)
entities_router.register('candidate', views.CandidateViewSet)

# URL patterns
urlpatterns = [
    # Template routes for JobRecord CRUD operations
    path('', views.job_list, name='job_list'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('create/', views.job_create, name='job_create'),
    path('<int:pk>/update/', views.job_update, name='job_update'),
    path('<int:pk>/delete/', views.job_delete, name='job_delete'),

    # API template routes
    path('api/', views.job_list_api, name='job_list_api'),
    path('api/<int:pk>/', views.job_detail_api, name='job_detail_api'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/dashboard/', views.dashboard_api, name='dashboard_api'),
    path('jobs/dashboard/', views.dashboard_api, name='jobs_dashboard_api'),

    # API endpoints
    path('jobs/', include(jobs_router.urls)),
    path('', include(entities_router.urls)),
]
