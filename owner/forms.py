from django import forms
from .models import Owner, Stall


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['name', 'phone', 'social_media', 'description']


class StallForm(forms.ModelForm):
    class Meta:
        model = Stall
        fields = ['owner', 'name', 'description', 'location', 'capacity', 'rental_fee']