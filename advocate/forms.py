from django import forms
from .models import*
from .models import CaseHistory

class CaseHistoryForm(forms.ModelForm):
    class Meta:
        model = CaseHistory
        fields = [ 'caseno', 'category', 'court', 'description', 'result']
        exclude=['advocate',]

class AdvocateAvailabilityForm(forms.ModelForm):
    class Meta:
        model = AdvocateAvailability
        fields = ['day', 'time_slot', 'start_time', 'end_time']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-control'}),
            'time_slot': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
