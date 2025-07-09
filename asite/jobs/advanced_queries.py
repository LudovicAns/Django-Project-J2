import os
import sys
import django
from django.db.models import Avg, Count, F, Q, Case, When, Value, FloatField
from django.db.models.functions import Round

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asite.settings')
django.setup()

from jobs.models import JobRecord, JobTitle, Contract, Location

def run_advanced_queries():
    output_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'query_results.txt')
    
    with open(output_file_path, 'w', encoding='utf-8') as output_file:

        top_job_titles = JobRecord.objects.values('job_title__name').annotate(
            avg_salary=Round(Avg('salary_in_usd'), 2)
        ).order_by('-avg_salary')[:5]
        
        output_file.write("=== Top 5 Job Titles with Highest Salaries (USD) ===\n")
        print("=== Top 5 Job Titles with Highest Salaries (USD) ===")
        for i, job in enumerate(top_job_titles, 1):
            result = f"{i}. {job['job_title__name']}: ${job['avg_salary']:,.2f} USD"
            output_file.write(result + "\n")
            print(result)
        output_file.write("\n")
        print()

        avg_by_experience = JobRecord.objects.values('experience_level__type_code', 'experience_level__description').annotate(
            avg_salary=Round(Avg('salary_in_usd'), 2)
        ).order_by('experience_level__type_code')
        
        output_file.write("=== Average Salary by Experience Level ===\n")
        print("=== Average Salary by Experience Level ===")
        for exp in avg_by_experience:
            result = f"{exp['experience_level__type_code']} ({exp['experience_level__description']}): ${exp['avg_salary']:,.2f} USD"
            output_file.write(result + "\n")
            print(result)
        output_file.write("\n")
        print()

        jobs_by_location = JobRecord.objects.values('company_location__country_code').annotate(
            job_count=Count('id')
        ).order_by('-job_count')
        
        output_file.write("=== Number of Jobs by Company Location ===\n")
        print("=== Number of Jobs by Company Location ===")
        for loc in jobs_by_location:
            result = f"{loc['company_location__country_code']}: {loc['job_count']} jobs"
            output_file.write(result + "\n")
            print(result)
        output_file.write("\n")
        print()

        total_jobs = JobRecord.objects.count()
        remote_jobs = JobRecord.objects.filter(remote_ratio=100).count()
        remote_ratio = (remote_jobs / total_jobs) * 100 if total_jobs > 0 else 0
        
        output_file.write("=== Remote Jobs Ratio ===\n")
        print("=== Remote Jobs Ratio ===")
        result = f"100% Remote Jobs: {remote_jobs} out of {total_jobs} ({remote_ratio:.2f}%)"
        output_file.write(result + "\n")
        print(result)
    
    print(f"\nResults saved to {output_file_path}")

if __name__ == "__main__":
    run_advanced_queries()