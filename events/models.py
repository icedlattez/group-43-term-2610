from django.db import models
from django.contrib.auth.models import User


# ------------------------
# EVENT MODEL
# ------------------------
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

    # ------------------------
    # BASIC INFO
    # ------------------------
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPE_CHOICES
    )

    # ------------------------
    # TIME
    # ------------------------
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    # ------------------------
    # MEDIA
    # ------------------------
    image = models.ImageField(upload_to='events/', null=True, blank=True)

    # ------------------------
    # RELATIONSHIPS
    # ------------------------
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)

    # ------------------------
    # STATUS
    # ------------------------
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # ------------------------
    # OPTIONAL FEATURES
    # ------------------------
    allow_vendors_collaborators = models.BooleanField(
        default=False
    )

    # registration fee
    has_registration_fee = models.BooleanField(default=False)
    registration_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00
    )

    # ------------------------
    # TIMESTAMP
    # ------------------------
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ------------------------
# EVENT REGISTRATION MODEL
# ------------------------
class EventRegistration(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    # stores different form types (concert / tournament / bazaar)
    data = models.JSONField(null=True, blank=True)

    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} → {self.event.title}"