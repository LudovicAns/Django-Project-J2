from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Feedbacks
from .forms import FeedbackForm
from .serializer import FeedbackSerializer
from jobs.models import JobRecord, JobTitle


# API ViewSet
class FeedbackViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Feedbacks.objects.all()
    serializer_class = FeedbackSerializer

    search_fields = ['comment']
    ordering_fields = ['created_at', 'rating']


# Template Views for Feedback CRUD operations
def feedback_list(request):
    """View function for listing all feedbacks."""
    # Get search and sort parameters from request
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '-created_at')  # Default sort by newest
    page = request.GET.get('page', 1)  # Get the page parameter, default to 1

    # Start with all feedbacks
    feedbacks = Feedbacks.objects.all()

    # Apply search filter if provided
    if search_query:
        feedbacks = feedbacks.filter(comment__icontains=search_query)

    # Apply sorting
    feedbacks = feedbacks.order_by(sort_by)

    # Apply pagination
    paginator = Paginator(feedbacks, 10)  # Show 10 feedbacks per page
    try:
        feedbacks_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        feedbacks_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        feedbacks_page = paginator.page(paginator.num_pages)

    context = {
        'feedbacks': feedbacks_page,
        'search_query': search_query,
        'sort_by': sort_by,
    }

    return render(request, 'feedbacks/feedback_list.html', context)

def feedback_list_api(request):
    """View function for listing all feedbacks using API."""
    return render(request, 'feedbacks/feedback_list_api.html')


def feedback_detail(request, pk):
    """View function for displaying details of a specific feedback."""
    feedback = get_object_or_404(Feedbacks, pk=pk)
    return render(request, 'feedbacks/feedback_detail.html', {'feedback': feedback})

def feedback_detail_api(request, pk):
    """View function for displaying details of a specific feedback using API."""
    return render(request, 'feedbacks/feedback_detail_api.html')


def feedback_create(request):
    """View function for creating a new feedback."""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            return redirect('feedback_detail', pk=feedback.pk)
    else:
        form = FeedbackForm()

    return render(request, 'feedbacks/feedback_form.html', {'form': form})


def feedback_update(request, pk):
    """View function for updating an existing feedback."""
    feedback = get_object_or_404(Feedbacks, pk=pk)
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            feedback = form.save()
            return redirect('feedback_detail', pk=feedback.pk)
    else:
        form = FeedbackForm(instance=feedback)

    return render(request, 'feedbacks/feedback_form.html', {'form': form})


def feedback_delete(request, pk):
    """View function for deleting an existing feedback."""
    feedback = get_object_or_404(Feedbacks, pk=pk)
    if request.method == 'POST':
        feedback.delete()
        return redirect('feedback_list')

    return render(request, 'feedbacks/feedback_confirm_delete.html', {'feedback': feedback})
