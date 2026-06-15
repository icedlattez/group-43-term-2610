from django.db import models
from django.conf import settings


# =========================================================
# EVENT
# =========================================================
class Event(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    EVENT_TYPE_CHOICES = [
        ('concert', 'Concert'),
        ('tournament', 'Tournament'),
        ('bazaar', 'Bazaar'),
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

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    image = models.ImageField(
        upload_to='events/',
        null=True,
        blank=True
    )

    # ------------------------
    # ORGANIZER
    # ------------------------
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # ------------------------
    # REGISTRATION SETTINGS
    # ------------------------
    allow_registration = models.BooleanField(default=True)

    max_registrations = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    # ✅ Vendor toggle (USED BY YOUR TEMPLATE + VIEW)
    allow_vendors_collaborators = models.BooleanField(default=False)

    # ------------------------
    # FEES
    # ------------------------
    enable_registration_fee = models.BooleanField(default=False)

    registration_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00,
        null=True,
        blank=True
    )

    # ------------------------
    # TOURNAMENT ONLY
    # ------------------------
    team_size = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    # ------------------------
    # TIMESTAMP
    # ------------------------
    created_at = models.DateTimeField(auto_now_add=True)

    # =====================================================
    # HELPERS
    # =====================================================
    def total_registrations(self):
        return self.registrations.count()

    def is_full(self):
        if not self.max_registrations:
            return False
        return self.total_registrations() >= self.max_registrations

    def has_fee(self):
        return self.enable_registration_fee and self.registration_fee > 0

    def __str__(self):
        return self.title


# =========================================================
# EVENT REGISTRATION (ATTENDEE)
# =========================================================
class EventRegistration(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="registrations"
    )

    data = models.JSONField(blank=True, null=True)

    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} → {self.event.title}"


# =========================================================
# VENDOR REGISTRATION
# =========================================================
class VendorRegistration(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="vendor_registrations"
    )

    data = models.JSONField(blank=True, null=True)

    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} → {self.event.title} (Vendor)"