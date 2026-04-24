from django.db import models


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    social_media = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Stall(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    event_name = models.CharField(max_length=100)

    status = models.CharField(max_length=20, default="Active")
    rental_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    capacity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.event_name}"