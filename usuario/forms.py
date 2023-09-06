from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class user_register_form(UserCreationForm):
    email=forms.EmailField(label='Email usuario')
    password1=forms.CharField(label='contraseña', widget=forms.PasswordInput)
    password2=forms.CharField(label='confirmar contraseña', widget=forms.PasswordInput)
    field_order=['username', 'email', 'password1', 'password2']
    class Meta:
        model = User
        fields={'username', 'email', 'password1', 'password2'}
        help_texts= { k:'' for k in fields }

class User_perfil_form(forms.Form):
    username=forms.CharField(label='Nombre de usuario', disabled=True)
    nombre=forms.CharField(label='Nombre', disabled=True)
    email=forms.EmailField(label='Mail', disabled=True)
    descripcion=forms.CharField(widget=forms.Textarea, disabled=True)
