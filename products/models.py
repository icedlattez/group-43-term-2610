from django.db import models
from owner.models import Stall


class Product(models.Model):
    stall = models.ForeignKey(Stall, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name