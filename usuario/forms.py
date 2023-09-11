from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm


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

class User_perfil_form(ModelForm): # ModelForm fue la solucion a todos mis problemas
    #descripcion=forms.CharField(required=False, widget=forms.Textarea)
    #imagen=forms.ImageField(label='imagen')
    field_order=['descripcion', 'imagen']
    class Meta:
        model = Perfil
        fields = {'descripcion', 'imagen'}
    
class User_edit_form(UserCreationForm):
    first_name=forms.CharField(label='Nombre')
    email=forms.EmailField(label='Email')
    password1=forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2=forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)
    field_order=['first_name', 'email', "password1", 'password2']
    class Meta:
        model = User
        #fields={'username', 'email', 'first_name', 'password1', 'password2'}
        fields={'email', 'first_name', 'password1', 'password2'}
        #help_texts= { k:'' for k in fields }
