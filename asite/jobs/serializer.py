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
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'email', 'location',]

class JobRecordSerializer(serializers.ModelSerializer):
    contract_experience = ContractSerializer(read_only=True, source='experience_level')
    contract_employment = ContractSerializer(read_only=True, source='employment_type')
    industry = IndustrySerializer(read_only=True)
    candidate = CandidateSerializer(read_only=True)
    skills = SkillSerializer(many=True)

    class Meta:
        model = JobRecord
        fields= [
            'id', 'job_title', 'work_year',
            'company_location', 'company_size',
            'salary', 'salary_currency', 'salary_in_usd',
            'remote_ratio', 'experience_level',
            'employment_type', 'industry', 'candidate',
            'skills', 'contract_experience',
            'contract_employment',
        ]