from django import forms
from .models import Feedbacks

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedbacks
        fields = ['job', 'author_name', 'comment', 'rating']
        
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating