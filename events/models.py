from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=True)  # for now True (skip admin first)

    def __str__(self):
        return self.title
        
    
    