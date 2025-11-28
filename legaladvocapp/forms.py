from django import forms
import re
from .models import*
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class UserRegistrationForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=10, required=True)  # Assuming phone number is a string
    email = forms.EmailField(max_length=50, required=True)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(max_length=20, widget=forms.PasswordInput, required=True)
    purpose=forms.CharField(max_length=100,required=True)
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if the email already exists in tblUser_Log
        if tblUser_Log.objects.filter(email=email).exists():
            raise ValidationError("This email is already taken.")
        return email
    def clean_name(self):
        name = self.cleaned_data.get('name')
        # Check if name contains only alphabets and spaces
        if not re.match("^[a-zA-Z ]*$", name):
            raise ValidationError("Name can only contain alphabets and spaces.")
        return name
    

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValidationError("Phone number must be 10 digits.")
        return phone_number


    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('password', "Passwords do not match.")
            self.add_error('confirm_password', "Passwords do not match.")
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=50, required=True)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, required=True)
    




    #advocate registration forms
class UserLogForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=20)
    confirm_password = forms.CharField(widget=forms.PasswordInput, max_length=20)

    class Meta:
        model = tblUser_Log
        fields = ['email', 'password', 'confirm_password']
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if the email already exists in tblUser_Log
        if tblUser_Log.objects.filter(email=email).exists():
            raise ValidationError("This email is already taken.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('password', "Passwords do not match.")
            self.add_error('confirm_password', "Passwords do not match.")



class AdvocateForm(forms.ModelForm):
    class Meta:
        model = tbladvocate
        exclude = ['login', 'status','payment_status']  # We will handle the login manually.

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not re.match("^[a-zA-Z ]*$", name):
            raise ValidationError("Name can only contain alphabets and spaces.")
        return name

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if not (23 < age < 70):
            raise ValidationError("Age must be between 23 and 70.")
        return age

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValidationError("Phone number must be 10 digits.")
        return phone_number

    def clean_enrollment_year(self):
        enrollment_year = self.cleaned_data.get('enrollment_year')
        if len(str(enrollment_year)) != 4:
            raise ValidationError("Enrollment year must be 4 digits.")
        return enrollment_year

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if len(pincode) != 6 or not pincode.isdigit():
            raise ValidationError("Pincode must be 6 digits.")
        return pincode

    def clean_bcnumber(self):
        bcnumber = self.cleaned_data.get('bcnumber')
        if tbladvocate.objects.filter(bcnumber=bcnumber).exists():
            raise ValidationError("BC number must be unique.")
        return bcnumber
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('password', "Passwords do not match.")
            self.add_error('confirm_password', "Passwords do not match.")


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 4}),
        }

   
