from django.db import models
from django.contrib.auth.models import User

class Listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Product-only field
    stock = models.IntegerField(default=0)

    # Personal listing
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    # differentiate type
    is_product = models.BooleanField(default=False)

    def __str__(self):
        return self.title