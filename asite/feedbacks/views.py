from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Feedbacks
from .forms import FeedbackForm
from .serializer import FeedbackSerializer
from jobs.models import JobRecord


# Create your views here.
class FeedbackViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Feedbacks.objects.all()
    serializer_class = FeedbackSerializer

def select_job(request):
    jobs = JobRecord.objects.all().order_by('job_title__name')
    return render(request, 'feedbacks/select_job.html', {'jobs': jobs})

def job_feedbacks(request, job_id):
    job = get_object_or_404(JobRecord, id=job_id)
    min_rating = request.GET.get('min_rating')

    feedbacks = Feedbacks.objects.filter(job=job)

    if min_rating and min_rating.isdigit():
        feedbacks = feedbacks.filter(rating__gte=int(min_rating))

    # Calculate average rating
    average_rating = feedbacks.aggregate(Avg('rating'))['rating__avg']

    context = {
        'job': job,
        'feedbacks': feedbacks,
        'min_rating': min_rating,
        'average_rating': average_rating,
    }
    return render(request, 'feedbacks/list_feedback.html', context)

def add_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_feedbacks', job_id=form.cleaned_data['job'].id)
    else:
        form = FeedbackForm()

    return render(request, 'feedbacks/add_feedback.html', {'form': form})

def job_average_rating(request, job_id):
    job = get_object_or_404(JobRecord, id=job_id)
    average_rating = Feedbacks.objects.filter(job=job).aggregate(Avg('rating'))['rating__avg']

    context = {
        'job': job,
        'average_rating': average_rating,
    }
    return render(request, 'feedbacks/job_average_rating.html', context)
