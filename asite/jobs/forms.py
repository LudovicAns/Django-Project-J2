from django import forms
from .models import JobRecord

class JobForm(forms.ModelForm):
    class Meta:
        model = JobRecord
        fields = [
            'work_year', 'experience_level', 'employment_type', 'job_title',
            'salary', 'salary_currency', 'salary_in_usd', 'employee_residence',
            'remote_ratio', 'company_location', 'company_size', 'skills',
            'industry', 'candidate'
        ]