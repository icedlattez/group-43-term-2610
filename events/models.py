from django.db import models
from django.conf import settings

class Event(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    EVENT_TYPE_CHOICES = [
        ('concert', 'Concert / Viewing Event'),
        ('tournament', 'Tournament / Competition'),
        ('bazaar', 'Bazaar / Stall Event'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPE_CHOICES
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    allow_vendors_collaborators = models.BooleanField(default=False)
    has_registration_fee = models.BooleanField(default=False)
    registration_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class EventRegistration(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    data = models.JSONField(null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} → {self.event.title}"