from django.db import models # type: ignore
from adminapp.models import Category
# Create your models here.


class tblUser_Reg(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    
    purpose=models.TextField()
    login = models.ForeignKey('tblUser_Log', on_delete=models.CASCADE)


class tblUser_Log(models.Model):
    email = models.EmailField(max_length=50)  # Adjusted max_length to a more suitable size
    password = models.CharField(max_length=20)
    keyuser = models.CharField(max_length=20)


   
class tbladvocate(models.Model):
    # Basic Information
    name = models.CharField(max_length=100)
    login = models.ForeignKey('tblUser_Log', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    category=models.ForeignKey('adminapp.Category',on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='advocate_photos/', null=True, blank=True)
    age = models.PositiveIntegerField()
    certificate = models.FileField(upload_to='advocate_certificates/', null=True, blank=True)
    gender_choices = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=6, choices=gender_choices)
    enrollment_year = models.PositiveIntegerField()
    qualification = models.CharField(max_length=200)
    practice_description = models.TextField()
    
    # Address Information
    office_location = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    district = models.CharField(max_length=100)
    payment_status=models.CharField(max_length=25,default='Pending')
    


# Status and Grade
    status_choices = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=8, choices=status_choices, default='pending')
    sitting_rate = models.FloatField(max_length=50)
    bcnumber=models.CharField(max_length=100)



class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.email}"
   

