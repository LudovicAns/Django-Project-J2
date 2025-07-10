from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import JobRecord, Category, Contract, Skill, Industry, JobTitle, Location, Candidate
from .serializer import JobRecordSerializer, CategorySerializer, ContractSerializer, SkillSerializer, \
    IndustrySerializer, JobTitleSerializer, LocationSerializer, CandidateSerializer


# Create your views here.
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
