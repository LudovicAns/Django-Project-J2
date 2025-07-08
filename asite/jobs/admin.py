from django.contrib import admin
from .models import JobRecord, Contract, Skill, Industry, Candidate

# Register your models here.

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('type_code', 'description')
    search_fields = ('type_code', 'description')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'location')
    search_fields = ('name', 'email', 'location')
    list_filter = ('location',)


@admin.register(JobRecord)
class JobRecordAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'work_year', 'salary_in_usd', 'experience_level', 
                   'employment_type', 'company_location', 'company_size', 'remote_ratio')
    list_filter = ('work_year', 'experience_level', 'employment_type', 
                  'company_size', 'remote_ratio', 'company_location')
    search_fields = ('job_title', 'candidate__name', 'skills__name', 'industry__name')
    filter_horizontal = ('skills',)
    fieldsets = (
        ('Job Information', {
            'fields': ('job_title', 'work_year', 'experience_level', 'employment_type')
        }),
        ('Salary Information', {
            'fields': ('salary', 'salary_currency', 'salary_in_usd')
        }),
        ('Company Information', {
            'fields': ('company_location', 'company_size', 'remote_ratio', 'industry')
        }),
        ('Candidate Information', {
            'fields': ('candidate', 'employee_residence')
        }),
        ('Skills', {
            'fields': ('skills',)
        }),
    )
