from django import forms
from .models import *
#add category
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['categoryname', 'description']  # List the fields you want in the form

    # Optional: You can also customize the form fields if needed
    categoryname = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 4})
    )
#add sections

class sectionForm(forms.ModelForm):
    class Meta:
        model = ipcsections
        fields = ['sections', 'description']  # List the fields you want in the form

    # Optional: You can also customize the form fields if needed
    sections = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter sections'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 4})
    )

#add court

class courtForm(forms.ModelForm):
    class Meta:
        model = court
        fields = ['courtname']  # List the fields you want in the form

    # Optional: You can also customize the form fields if needed
    courtname = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the court'})
    )
    
 #help
class helpForm(forms.ModelForm):
    class Meta:
        model = Help
        fields = ['question', 'answer']  # List the fields you want in the form

    # Optional: You can also customize the form fields if needed
    question = forms.CharField(
        max_length=200, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Question'})
    )
    answer = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Answer'})
    )  


    
    