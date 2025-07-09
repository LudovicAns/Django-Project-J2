from django.contrib import admin
from .models import Feedbacks

# Register your models here.
@admin.register(Feedbacks)
class FeedbacksAdmin(admin.ModelAdmin):
    list_display = ('job', 'author_name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('comment', 'job__job_title__name', 'author_name__name')
