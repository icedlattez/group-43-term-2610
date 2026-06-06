from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class ProfessionalSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    
    phone_number = forms.CharField(widget=forms.HiddenInput(), required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "first_name", "email", "phone_number")