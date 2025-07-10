from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# API router for Feedbacks
feedbacks_router = DefaultRouter()
feedbacks_router.register('feedbacks', views.FeedbackViewSet)

# URL patterns
urlpatterns = [
    # API endpoints
    path('feedbacks/', include(feedbacks_router.urls)),

    # Template routes for Feedback CRUD operations
    path('', views.feedback_list, name='feedback_list'),
    path('<int:pk>/', views.feedback_detail, name='feedback_detail'),
    path('create/', views.feedback_create, name='feedback_create'),
    path('<int:pk>/update/', views.feedback_update, name='feedback_update'),
    path('<int:pk>/delete/', views.feedback_delete, name='feedback_delete'),

    # API template routes
    path('api/', views.feedback_list_api, name='feedback_list_api'),
    path('api/<int:pk>/', views.feedback_detail_api, name='feedback_detail_api'),
]
