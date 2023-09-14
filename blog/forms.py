from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
import datetime


class Blog_create_form(ModelForm):
    imagen=forms.ImageField(required=True)
    field_order=['titulo', 'subtitulo', 'cuerpo', 'imagen']
    class Meta:
        model = Blog
        fields = {'titulo', 'subtitulo', 'cuerpo', 'imagen'}

class Blog_comentar_form(ModelForm):
    cuerpo=forms.CharField(label='comentar')
    class Meta:
        model = Comentario
        fields = {'cuerpo'}
