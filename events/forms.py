from django import forms
from .models import Event
from datetime import datetime


# =========================================================
# 1. EVENT CREATION FORM (ADMIN / ORGANIZER)
# =========================================================
class EventForm(forms.ModelForm):

    # ------------------------
    # DATE + TIME FIELDS
    # ------------------------
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control'
        })
    )

    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control'
        })
    )

    # ------------------------
    # OPTIONAL FEATURES
    # ------------------------
    allow_vendors_collaborators = forms.BooleanField(
        required=False,
        label="Allow vendors / collaborators?",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    has_registration_fee = forms.BooleanField(
        required=False,
        label="Enable registration fee?",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'feeToggle'
        })
    )

    registration_fee = forms.DecimalField(
        required=False,
        min_value=0,
        label="Registration Fee (RM)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'id': 'feeInput'
        })
    )

    class Meta:
        model = Event

        fields = [
            'title',
            'description',
            'location',
            'event_type',
            'image',
            'allow_vendors_collaborators',
            'has_registration_fee',
            'registration_fee',
        ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'event_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.start_date = datetime.combine(
            self.cleaned_data['start_date'],
            self.cleaned_data['start_time']
        )

        instance.end_date = datetime.combine(
            self.cleaned_data['end_date'],
            self.cleaned_data['end_time']
        )

        if not instance.has_registration_fee:
            instance.registration_fee = 0

        if commit:
            instance.save()

        return instance


# =========================================================
# 2. SMART REGISTRATION FORMS
# =========================================================

# ------------------------
# CONCERT / VIEWING EVENT
# ------------------------
class ConcertRegistrationForm(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )


# ------------------------
# TOURNAMENT / COMPETITION
# ------------------------
class TournamentRegistrationForm(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    team_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    skill_level = forms.ChoiceField(
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('pro', 'Pro'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )


# ------------------------
# BAZAAR / STALL EVENT
# ------------------------
class BazaarRegistrationForm(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    stall_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    item_selling = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    contact_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )