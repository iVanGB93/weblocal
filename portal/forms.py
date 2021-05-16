from django import forms
from django.contrib.auth.models import User

class EditUserForm(forms.ModelForm):
    email = forms.EmailField(label="Correo", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email...'
    }))
    first_name = forms.CharField(max_length=20, label='Nombre', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nombre...'
    }))
    last_name = forms.CharField(max_length=20, label='Apellidos', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Apellidos...'
    }))

    class Meta: 
        model = User
        fields = [            
            'email',
            'first_name',
            'last_name',
        ]