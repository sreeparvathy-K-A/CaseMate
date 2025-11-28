from django.db import models
from adminapp.models import *
from legaladvocapp.models import tbladvocate

class CaseHistory(models.Model):
    advocate= models.ForeignKey(tbladvocate, on_delete=models.CASCADE)
    caseno = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    court = models.ForeignKey(court, on_delete=models.CASCADE)
    description = models.TextField()
    result = models.TextField()

    def __str__(self):
        return f"Case {self.caseno} - {self.advocate.name}"
    
from django.db import models
from django.contrib.auth.models import User

TIME_SLOTS = [
    ('morning', 'Morning'),
    ('afternoon', 'Afternoon'),
    ('evening', 'Evening'),
]

WEEKDAYS = [
    ('monday', 'Monday'),
    ('tuesday', 'Tuesday'),
    ('wednesday', 'Wednesday'),
    ('thursday', 'Thursday'),
    ('friday', 'Friday'),
    ('saturday', 'Saturday'),
    ('sunday', 'Sunday'),
]

class AdvocateAvailability(models.Model):
    advocate = models.ForeignKey(tbladvocate, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=WEEKDAYS)
    time_slot = models.CharField(max_length=10, choices=TIME_SLOTS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('advocate', 'day', 'time_slot')  # Prevent duplicate entries

    def __str__(self):
        return f"{self.advocate.name} - {self.day} ({self.time_slot})"
