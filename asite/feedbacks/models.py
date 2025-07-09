from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from jobs.models import JobRecord, Candidate

# Create your models here.
class Feedbacks(models.Model):
    job = models.ForeignKey(JobRecord, on_delete=models.CASCADE, related_name='feedbacks')
    author_name = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='feedbacks')
    comment = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.job} by {self.author_name}"
