from django import forms # type: ignore
from .models import client_case,Chat
from .models import Review

class ClientCaseForm(forms.ModelForm):
    class Meta:
        model = client_case
        fields = ['date', 'category', 'description', 'status']
        exclude = ['client', 'date', 'status']
        widgets = {
            
            'description': forms.Textarea(attrs={'placeholder': 'Describe your case...'}),
        }
class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['message']

   #review
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} Star{'s' if i>1 else ''}") for i in range(1, 6)]),
            'review': forms.Textarea(attrs={'placeholder': 'Write your review here...', 'rows': 4}),
        }
