from django.db import models

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    social_media = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # product name
    category = models.CharField(max_length=50, blank=True)  # NEW
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)

def __str__(self):
    return f"{self.id}. {self.name} - RM{self.price}"
