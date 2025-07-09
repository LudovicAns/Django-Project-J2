"""
URL configuration for asite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from feedbacks.views import FeedbackViewSet
from jobs.views import CategoryViewSet, ContractViewSet, SkillViewSet, IndustryViewSet, JobTitleViewSet, \
    LocationViewSet, CandidateViewSet, JobRecordViewSet

api_router = DefaultRouter()

api_router.register('feedbacks', FeedbackViewSet)

api_router.register('category', CategoryViewSet)
api_router.register('contract', ContractViewSet)
api_router.register('skill', SkillViewSet)
api_router.register('industry', IndustryViewSet)
api_router.register('job-title', JobTitleViewSet)
api_router.register('location', LocationViewSet)
api_router.register('candidate', CandidateViewSet)
api_router.register('jobs', JobRecordViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_router.urls)),
    path('feedbacks/', include('feedbacks.urls')),
    path('jobs/', include('jobs.urls')),

]
