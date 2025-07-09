from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Contract(models.Model):
    type_code = models.CharField(max_length=10, primary_key=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.type_code} - {self.description}"


class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Industry(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class JobTitle(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    country_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.country_code


class Candidate(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class JobRecord(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
    ]

    COMPANY_SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    ]

    # Fields from CSV
    work_year = models.IntegerField()
    experience_level = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='experience_jobs')
    employment_type = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='employment_jobs')
    job_title = models.ForeignKey(JobTitle, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=12, decimal_places=2)
    salary_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    salary_in_usd = models.DecimalField(max_digits=12, decimal_places=2)
    employee_residence = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='employee_jobs')
    remote_ratio = models.IntegerField()
    company_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='company_jobs')
    company_size = models.CharField(max_length=1, choices=COMPANY_SIZE_CHOICES)

    class Meta:
        # Ensure uniqueness for job_title + work_year + company_location combination
        unique_together = ('job_title', 'work_year', 'company_location')

    # Relationships
    skills = models.ManyToManyField(Skill, blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True, blank=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.job_title} ({self.work_year}) - {self.salary_in_usd} USD"
