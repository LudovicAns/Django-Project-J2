from rest_framework import viewsets, filters
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.db.models import Avg, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import JobRecord, Category, Contract, Skill, Industry, JobTitle, Location, Candidate
from .serializer import JobRecordSerializer, CategorySerializer, ContractSerializer, SkillSerializer, \
    IndustrySerializer, JobTitleSerializer, LocationSerializer, CandidateSerializer, DashboardSerializer
from .forms import JobForm


# API ViewSets
class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ContractViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

class SkillViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class IndustryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer

class JobTitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer

class LocationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class CandidateViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

class JobRecordViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = JobRecord.objects.all()
    serializer_class = JobRecordSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['job_title__name', 'employee_residence__country_code']
    ordering_fields = ['salary_in_usd', 'created_at']


# Template Views for JobRecord CRUD operations
def job_list(request):
    """View function for listing all jobs."""
    # Get search and sort parameters from request
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '-salary_in_usd')  # Default sort by salary (high to low)
    page = request.GET.get('page', 1)  # Get the page parameter, default to 1

    # Start with all jobs
    jobs = JobRecord.objects.all()

    # Apply search filter if provided
    if search_query:
        jobs = jobs.filter(job_title__name__icontains=search_query)

    # Apply sorting
    jobs = jobs.order_by(sort_by)

    # Apply pagination
    paginator = Paginator(jobs, 10)  # Show 10 jobs per page
    try:
        jobs_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        jobs_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        jobs_page = paginator.page(paginator.num_pages)

    context = {
        'jobs': jobs_page,
        'search_query': search_query,
        'sort_by': sort_by,
    }

    return render(request, 'jobs/job_list.html', context)

def job_list_api(request):
    """View function for listing all jobs using API."""
    return render(request, 'jobs/job_list_api.html')

def job_detail(request, pk):
    """View function for displaying details of a specific job."""
    job = get_object_or_404(JobRecord, pk=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})

def job_detail_api(request, pk):
    """View function for displaying details of a specific job using API."""
    return render(request, 'jobs/job_detail_api.html')

def job_create(request):
    """View function for creating a new job."""
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm()

    return render(request, 'jobs/job_form.html', {'form': form})

def job_update(request, pk):
    """View function for updating an existing job."""
    job = get_object_or_404(JobRecord, pk=pk)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            job = form.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/job_form.html', {'form': form})

def job_delete(request, pk):
    """View function for deleting an existing job."""
    job = get_object_or_404(JobRecord, pk=pk)
    if request.method == 'POST':
        # Handle form submission
        # Delete the job
        job.delete()
        # Redirect to the job list page
        return redirect('job_list')
    else:
        # Display the confirmation page
        return render(request, 'jobs/job_confirm_delete.html', {'object': job})

@api_view(['GET'])
def dashboard_api(request):
    """API endpoint for dashboard data with job statistics."""
    # Group by job_title__name and calculate aggregated statistics for each group
    job_stats = JobRecord.objects.values('job_title__name').annotate(
        avg_rating=Avg('feedbacks__rating'),
        feedback_count=Count('feedbacks')
    )

    # Prepare data for serialization
    data = []
    for stat in job_stats:
        data.append({
            'job_title': stat['job_title__name'],
            'avg_rating': stat['avg_rating'] if stat['avg_rating'] is not None else 0,
            'feedback_count': stat['feedback_count']
        })

    serializer = DashboardSerializer(data, many=True)
    return Response(serializer.data)

def dashboard(request):
    """View function for displaying the dashboard page."""
    return render(request, 'jobs/dashboard.html')
