from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label='Usuario', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nombre de Usuario...'
    }))
    password = forms.CharField(max_length=20, label='Contraseña', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Contraseña...'
    }))

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=20, label='Usuario', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nombre de Usuario...'
    }))
    email = forms.EmailField(label="Correo", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email...'
    }))
    email2 = forms.EmailField(label="Confirme Correo", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Repita el email...'
    }))
    password = forms.CharField(max_length=10, label='Contraseña', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Contraseña...'
    }))

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]
