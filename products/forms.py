from django import forms
from .models import Owner, Stall


# =========================
# OWNER FORM
# =========================
class OwnerForm(forms.ModelForm):

    class Meta:
        model = Owner
        fields = [
            'name',
            'phone',
            'social_media',
            'description'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter owner name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
            'social_media': forms.TextInput(attrs={'placeholder': 'Instagram / TikTok link'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


# =========================
# STALL FORM (FIXED)
# =========================
class StallForm(forms.ModelForm):

    class Meta:
        model = Stall
        fields = [
            'name',
            'description',
            'location',
            'capacity',
            'rental_fee'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Stall name'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'location': forms.TextInput(attrs={'placeholder': 'Location'}),
            'capacity': forms.NumberInput(),
            'rental_fee': forms.NumberInput(),
        }