from django.db import models
from django.conf import settings

class Listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True,
        blank=True, 
        on_delete=models.CASCADE
    )
    is_product = models.BooleanField(default=False)

    def __str__(self):
        return self.title