from rest_framework import serializers
from .models import Category, Contract, Skill, Industry, JobTitle, Location, Candidate, JobRecord


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name',]

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['type_code', 'description',]

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name',]

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['id', 'name',]

class JobTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitle
        fields = ['id', 'name',]

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'country_code',]

class CandidateSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'email', 'location',]

class JobRecordSerializer(serializers.ModelSerializer):
    # Sérialiseurs imbriqués pour les opérations de lecture
    contract_experience = ContractSerializer(read_only=True, source='experience_level')
    contract_employment = ContractSerializer(read_only=True, source='employment_type')
    job_title_detail = JobTitleSerializer(read_only=True, source='job_title')
    employee_residence_detail = LocationSerializer(read_only=True, source='employee_residence')
    company_location_detail = LocationSerializer(read_only=True, source='company_location')
    industry_detail = IndustrySerializer(read_only=True, source='industry')
    candidate_detail = CandidateSerializer(read_only=True, source='candidate')
    skills_detail = SkillSerializer(read_only=True, many=True, source='skills')

    class Meta:
        model = JobRecord
        fields= [
            'id', 'job_title', 'job_title_detail', 'work_year',
            'employee_residence', 'employee_residence_detail',
            'company_location', 'company_location_detail', 'company_size',
            'salary', 'salary_currency', 'salary_in_usd',
            'remote_ratio', 'experience_level',
            'employment_type', 'industry', 'industry_detail', 'candidate', 'candidate_detail',
            'skills', 'skills_detail', 'contract_experience',
            'contract_employment',
        ]