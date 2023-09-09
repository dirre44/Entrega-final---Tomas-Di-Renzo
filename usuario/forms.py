from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class User_register_form(UserCreationForm):
    first_name=first_name=forms.CharField(label='Nombre')
    email=forms.EmailField(label='Email usuario')
    password1=forms.CharField(label='contraseña', widget=forms.PasswordInput)
    password2=forms.CharField(label='confirmar contraseña', widget=forms.PasswordInput)
    field_order=['username','first_name', 'email', 'password1', 'password2']
    class Meta:
        model = User
        fields={'username', 'first_name', 'email', 'password1', 'password2'}
        help_texts= { k:'' for k in fields }

class User_perfil_form(forms.Form):
    descripcion=forms.CharField(widget=forms.Textarea, disabled=True)

class User_mostrar_form(UserCreationForm):
    username=forms.CharField(label='Nombre de usuario', disabled=True)
    email=forms.EmailField(label='Email usuario', disabled=True)
    first_name=forms.CharField(label='Nombre', disabled=True)
    field_order=['username','first_name', 'email']
    class Meta:
        model = User
        fields={'username', 'email', 'first_name'}
        help_texts= { k:'' for k in fields }
