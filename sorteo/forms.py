from django import forms

class CodeForm(forms.Form):
    code = forms.CharField(max_length=10, label='Formulario', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'escriba el código...'
    }))