from django import forms
from django.contrib.auth.models import User

class EditUserForm(forms.ModelForm):
    email = forms.EmailField(label="Correo", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'su correo...'
    }))
    first_name = forms.CharField(max_length=20, label='Nombre:', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'su nombre...'
    }))
    last_name = forms.CharField(max_length=40, label='Apellidos:', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'sus apellidos...'
    }))
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name'
        ]