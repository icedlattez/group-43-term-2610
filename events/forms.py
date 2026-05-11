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

    # ------------------------
    # MAX REGISTRATIONS
    # ------------------------
    max_registrations = forms.IntegerField(
        required=False,
        min_value=1,
        label="Max Number of Registrations",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Leave empty for unlimited'
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
            'max_registrations',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'event_type': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get('start_date')
        start_time = cleaned_data.get('start_time')
        end_date = cleaned_data.get('end_date')
        end_time = cleaned_data.get('end_time')

        has_fee = cleaned_data.get('has_registration_fee')
        registration_fee = cleaned_data.get('registration_fee')

        # ------------------------
        # VALIDATE EVENT TIME
        # ------------------------
        if start_date and start_time and end_date and end_time:

            start_datetime = datetime.combine(start_date, start_time)
            end_datetime = datetime.combine(end_date, end_time)

            if end_datetime <= start_datetime:
                raise forms.ValidationError(
                    "Event end date/time must be after start date/time."
                )

        # ------------------------
        # VALIDATE REGISTRATION FEE
        # ------------------------
        if has_fee and registration_fee is None:
            raise forms.ValidationError(
                "Please enter a registration fee amount."
            )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Combine date + time into datetime
        instance.start_date = datetime.combine(
            self.cleaned_data['start_date'],
            self.cleaned_data['start_time']
        )

        instance.end_date = datetime.combine(
            self.cleaned_data['end_date'],
            self.cleaned_data['end_time']
        )

        # If fee disabled, set fee to 0
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
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )


# ------------------------
# TOURNAMENT / COMPETITION
# ------------------------
class TournamentRegistrationForm(forms.Form):

    full_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    team_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    skill_level = forms.ChoiceField(
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('pro', 'Pro'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )


# ------------------------
# BAZAAR / STALL EVENT
# ------------------------
class BazaarRegistrationForm(forms.Form):

    full_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    stall_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    item_selling = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    contact_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )