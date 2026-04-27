from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('organizer', 'Lecturer/Organizer'),
        ('admin', 'Admin'),
    )
    
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='student')
    is_approving = models.BooleanField(default=False)

    groups = models.ManyToManyField('auth.Group', related_name='custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions', blank=True)