from django.core.management.base import BaseCommand
from jobs.models import JobRecord, Candidate
from feedback.models import Feedback
import random

class Command(BaseCommand):
    help = 'Creates sample feedback records'

    def handle(self, *args, **options):
        # Get some job records and candidates
        job_records = JobRecord.objects.all()[:5]  # Get first 5 job records
        candidates = Candidate.objects.all()[:3]   # Get first 3 candidates
        
        if not job_records or not candidates:
            self.stdout.write(self.style.ERROR('No job records or candidates found. Please create some first.'))
            return
        
        # Sample comments
        comments = [
            "Great job opportunity with excellent benefits.",
            "The work environment was challenging but rewarding.",
            "I learned a lot from this position, but the salary could be better.",
            "Excellent team and management. Highly recommended!",
            "The job description didn't match the actual responsibilities.",
        ]
        
        # Create feedback records
        feedbacks_created = 0
        for job in job_records:
            for candidate in candidates:
                # Don't create feedback for every combination to avoid too many records
                if random.random() < 0.7:  # 70% chance to create feedback
                    rating = random.randint(1, 5)
                    comment = random.choice(comments)
                    
                    Feedback.objects.create(
                        job=job,
                        author_name=candidate,
                        comment=comment,
                        rating=rating
                    )
                    feedbacks_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {feedbacks_created} feedback records'))