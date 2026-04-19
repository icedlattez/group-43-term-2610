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
    stall_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    event_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default="Active")

    def __str__(self):
        return self.stall_name