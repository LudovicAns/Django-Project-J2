from django.urls import path, include
from rest_framework.routers import DefaultRouter

from asite.jobs.views import JobRecordViewSet, CategoryViewSet

router = DefaultRouter()
router.register('category', CategoryViewSet)
router.register('contract', CategoryViewSet)
router.register('skill', CategoryViewSet)
router.register('industry', CategoryViewSet)
router.register('job-title', CategoryViewSet)
router.register('location', CategoryViewSet)
router.register('candidate', CategoryViewSet)
router.register('jobs', JobRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]