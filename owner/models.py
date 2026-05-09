from django.db import models


class Owner(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    social_media = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Stall(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='stalls')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    capacity = models.IntegerField()
    rental_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name