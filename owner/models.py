from django.db import models
from django.conf import settings


# =========================================================
# OWNER MODEL
# =========================================================
class Owner(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owners"
    )

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    social_media = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# =========================================================
# STALL MODEL
# =========================================================
class Stall(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    event = models.ForeignKey(
        "events.Event",
        on_delete=models.CASCADE,
        related_name="stalls",
        null=True,
        blank=True
    )

    owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        related_name="stalls",
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)

    capacity = models.PositiveIntegerField(default=1)

    rental_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    stall_image = models.ImageField(
        upload_to="stall_images/",
        blank=True,
        null=True
    )

    rental_start_date = models.DateField(blank=True, null=True)
    rental_end_date = models.DateField(blank=True, null=True)

    is_active = models.BooleanField(default=False)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        event_name = self.event.title if self.event else "No Event"
        return f"{self.name} ({event_name})"