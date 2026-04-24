from django import forms
from .models import Stall

class StallForm(forms.ModelForm):
    class Meta:
        model = Stall
        fields = ['vendor', 'category', 'location', 'event_name', 'status']