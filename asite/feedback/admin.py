from django.contrib import admin
from .models import Feedback

# Register your models here.
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('job', 'author_name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('comment', 'job__job_title__name', 'author_name__name')
