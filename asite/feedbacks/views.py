from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg, Count
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Feedbacks
from .forms import FeedbackForm
from .serializer import FeedbackSerializer
from jobs.models import JobRecord, JobTitle


# Create your views here.
class FeedbackViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Feedbacks.objects.all()
    serializer_class = FeedbackSerializer

    search_fields = ['comment']
    ordering_fields = ['created_at', 'rating']

def select_job(request):
    # Group jobs by title and count how many jobs are in each group
    job_titles = JobTitle.objects.annotate(job_count=Count('jobrecord')).order_by('name')
    return render(request, 'feedbacks/select_job.html', {'job_titles': job_titles})

def job_title_feedbacks(request, job_title_id):
    job_title = get_object_or_404(JobTitle, id=job_title_id)
    min_rating = request.GET.get('min_rating')

    # Get all jobs with this title
    jobs = JobRecord.objects.filter(job_title=job_title)

    # Get all feedbacks for these jobs
    feedbacks = Feedbacks.objects.filter(job__in=jobs)

    if min_rating and min_rating.isdigit():
        feedbacks = feedbacks.filter(rating__gte=int(min_rating))

    # Calculate average rating
    average_rating = feedbacks.aggregate(Avg('rating'))['rating__avg']

    context = {
        'job_title': job_title,
        'jobs': jobs,
        'feedbacks': feedbacks,
        'min_rating': min_rating,
        'average_rating': average_rating,
    }
    return render(request, 'feedbacks/list_feedback.html', context)

def job_feedbacks(request, job_id):
    job = get_object_or_404(JobRecord, id=job_id)
    min_rating = request.GET.get('min_rating')
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '-created_at')  # Default sort by newest

    # Get all feedbacks for this job
    feedbacks = Feedbacks.objects.filter(job=job)

    # Apply minimum rating filter if provided
    if min_rating and min_rating.isdigit():
        feedbacks = feedbacks.filter(rating__gte=int(min_rating))

    # Apply search filter if provided
    if search_query:
        feedbacks = feedbacks.filter(comment__icontains=search_query)

    # Apply sorting
    feedbacks = feedbacks.order_by(sort_by)

    context = {
        'job': job,
        'feedbacks': feedbacks,
        'min_rating': min_rating,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'feedbacks/job_feedbacks.html', context)

def add_feedback(request):
    # Get all job titles for the dropdown
    job_titles = JobTitle.objects.all().order_by('name')

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            # Redirect directly to job_title_feedbacks
            return redirect('job_title_feedbacks', job_title_id=feedback.job.job_title.id)
    else:
        form = FeedbackForm()

    return render(request, 'feedbacks/add_feedback.html', {
        'form': form,
        'job_titles': job_titles
    })

def job_average_rating(request, job_id):
    job = get_object_or_404(JobRecord, id=job_id)
    # Redirect to job title average rating
    return redirect('job_title_average_rating', job_title_id=job.job_title.id)

def job_title_average_rating(request, job_title_id):
    job_title = get_object_or_404(JobTitle, id=job_title_id)
    # Get all jobs with this title
    jobs = JobRecord.objects.filter(job_title=job_title)
    # Get average rating for all feedbacks for these jobs
    average_rating = Feedbacks.objects.filter(job__in=jobs).aggregate(Avg('rating'))['rating__avg']

    context = {
        'job_title': job_title,
        'jobs': jobs,
        'average_rating': average_rating,
    }
    return render(request, 'feedbacks/job_average_rating.html', context)

def get_jobs_by_title(request):
    job_title_id = request.GET.get('job_title_id')
    if job_title_id:
        jobs = JobRecord.objects.filter(job_title_id=job_title_id).values('id', 'work_year', 'company_location__country_code', 'salary_in_usd')
        return JsonResponse(list(jobs), safe=False)
    return JsonResponse([], safe=False)

def all_feedbacks(request):
    # Get search and sort parameters from request
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '-created_at')  # Default sort by newest

    # Start with all feedbacks
    feedbacks = Feedbacks.objects.all()

    # Apply search filter if provided
    if search_query:
        feedbacks = feedbacks.filter(comment__icontains=search_query)

    # Apply sorting
    feedbacks = feedbacks.order_by(sort_by)

    context = {
        'feedbacks': feedbacks,
        'search_query': search_query,
        'sort_by': sort_by,
    }

    return render(request, 'feedbacks/all_feedbacks.html', context)
