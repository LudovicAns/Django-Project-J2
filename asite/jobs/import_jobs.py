import os
import csv
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asite.settings')
django.setup()

from .models import JobTitle, Location, JobRecord, Contract

def import_jobs_from_csv(csv_file_path):
    # Initialize counters
    job_titles_created = 0
    locations_created = 0
    job_records_created = 0
    duplicates_skipped = 0

    # Open and read the CSV file
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            # Check if JobTitle exists, create if not
            job_title_name = row['job_title']
            job_title, job_title_created = JobTitle.objects.get_or_create(name=job_title_name)
            if job_title_created:
                job_titles_created += 1
                print(f"Created job title: {job_title_name}")

            # Check if Location exists for employee_residence, create if not
            employee_residence_code = row['employee_residence']
            employee_residence, employee_residence_created = Location.objects.get_or_create(country_code=employee_residence_code)
            if employee_residence_created:
                locations_created += 1
                print(f"Created location: {employee_residence_code}")

            # Check if Location exists for company_location, create if not
            company_location_code = row['company_location']
            company_location, company_location_created = Location.objects.get_or_create(country_code=company_location_code)
            if company_location_created:
                locations_created += 1
                print(f"Created location: {company_location_code}")

            # Get or create Contract for experience_level
            experience_level_code = row['experience_level']
            experience_level, _ = Contract.objects.get_or_create(
                type_code=experience_level_code,
                defaults={'description': f'Experience Level: {experience_level_code}'}
            )

            # Get or create Contract for employment_type
            employment_type_code = row['employment_type']
            employment_type, _ = Contract.objects.get_or_create(
                type_code=employment_type_code,
                defaults={'description': f'Employment Type: {employment_type_code}'}
            )

            # Try to create JobRecord, handle duplicates
            try:
                # candidate field is optional and not in CSV, so we don't include it
                job_record = JobRecord.objects.create(
                    work_year=int(row['work_year']),
                    experience_level=experience_level,
                    employment_type=employment_type,
                    job_title=job_title,
                    salary=float(row['salary']),
                    salary_currency=row['salary_currency'],
                    salary_in_usd=float(row['salary_in_usd']),
                    employee_residence=employee_residence,
                    remote_ratio=int(row['remote_ratio']),
                    company_location=company_location,
                    company_size=row['company_size'],
                )
                job_records_created += 1
                print(f"Created job record: {job_record}")
            except django.db.utils.IntegrityError:
                # This combination of job_title, work_year, and company_location already exists
                duplicates_skipped += 1
                print(f"Skipped duplicate: {job_title_name} ({row['work_year']}) - {company_location_code}")

    # Print summary
    print("\n--- Import Summary ---")
    print(f"Job Titles created: {job_titles_created}")
    print(f"Locations created: {locations_created}")
    print(f"Job Records created: {job_records_created}")
    print(f"Duplicates skipped: {duplicates_skipped}")
    print("---------------------")

if __name__ == "__main__":
    # Path to the CSV file
    csv_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'salaries.csv')

    if not os.path.exists(csv_file_path):
        print(f"Error: CSV file not found at {csv_file_path}")
        sys.exit(1)

    print(f"Importing jobs from {csv_file_path}...")
    import_jobs_from_csv(csv_file_path)
    print("Import completed.")
