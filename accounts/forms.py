from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ProfessionalSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Enter your real name')
    email = forms.EmailField(max_length=254, required=True, help_text='Enter a valid MMU email')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'email',)