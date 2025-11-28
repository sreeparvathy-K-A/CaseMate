from django.db import models # type: ignore
from legaladvocapp.models import tblUser_Reg
from adminapp.models import Category
from datetime import date
from advocate.models import AdvocateAvailability
from django.utils import timezone # type: ignore
class client_case(models.Model):
    client = models.ForeignKey('legaladvocapp.tblUser_Reg', on_delete=models.CASCADE)
    date = models.DateField(default=date.today)  # You can also use DateTimeField if you need time information
    description = models.TextField()  # For detailed case description
    category = models.ForeignKey('adminapp.Category', on_delete=models.CASCADE)
    
    status_choices = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    status = models.CharField(max_length=20, choices=status_choices, default='pending')
    
    def __str__(self):
        return f"Case for {self.client} - {self.status}"
    

class Chat(models.Model):
    SENDER_CHOICES = (
        ('client', 'Client'),
        ('advocate', 'Advocate'),
    )
    client = models.ForeignKey('legaladvocapp.tblUser_Reg', on_delete=models.CASCADE)
    advocate = models.ForeignKey('legaladvocapp.tbladvocate', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    case = models.ForeignKey('client_case', null=True, blank=True, on_delete=models.CASCADE)
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    attachment = models.FileField(upload_to='chat_files/', blank=True, null=True)  # File upload
   
    def __str__(self):
        return f"Chat between {self.client} and {self.advocate} at {self.timestamp}"
    


    #review
class Review(models.Model):
    client = models.ForeignKey('legaladvocapp.tblUser_Reg', on_delete=models.CASCADE)
    advocate = models.ForeignKey('legaladvocapp.tbladvocate', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars
    review = models.TextField(blank=True)
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Review for {self.advocate} by {self.client} - {self.rating} Stars"

class PremiumUser(models.Model):
    client = models.OneToOneField('legaladvocapp.tblUser_Reg', on_delete=models.CASCADE)  # Assuming User is the client
    purchased_on = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return self.client.name
    
class advocate_case(models.Model):
    case=models.ForeignKey('client_case',on_delete=models.CASCADE)
    advocate=models.ForeignKey('legaladvocapp.tbladvocate', on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=25,default="Pending")
    payment_status = models.CharField(
        max_length=25, 
        default="Not Paid", 
        choices=[("Not Paid", "Not Paid"), ("Payment Completed", "Payment Completed")])
class Booking(models.Model):
    client = models.ForeignKey('legaladvocapp.tblUser_Reg', on_delete=models.CASCADE)  
    advocate = models.ForeignKey('legaladvocapp.tbladvocate', on_delete=models.CASCADE)
    availability = models.ForeignKey('advocate.AdvocateAvailability', on_delete=models.CASCADE)
    date = models.DateField(default=date.today)  # ✅ Add default value
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.name} booked {self.advocate.name} on {self.date}"