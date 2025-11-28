from django.db import models

# Create your models here.

class Category(models.Model):
    categoryname = models.CharField(max_length=100, unique=True)  # Ensuring category names are unique
    description = models.TextField(max_length=500)  # Using TextField for more flexible descriptions

    def __str__(self):
        return self.categoryname
    

    
class ipcsections(models.Model):
    sections = models.CharField(max_length=100, unique=True)  
    description = models.TextField(max_length=500)  
    def __str__(self):
        return self.sections
    
class court(models.Model):
        courtname = models.CharField(max_length=100, unique=True)    
        def __str__(self):
           return self.courtname
        
class Help(models.Model):
    question = models.CharField(max_length=200, unique=True)  
    answer = models.TextField(max_length=500)  

    def __str__(self):
        return self.question