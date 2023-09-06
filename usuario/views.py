from typing import Any, Dict
from .models import *
from .forms import * 
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context, loader
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.

def inicio(request):
    return render(request, "inicio.html")

def user_register (request):
    if request.method=="POST":
        form=user_register_form(request.POST)
        if form.is_valid():
            info=form.cleaned_data
            usu=info['username']
            info=form.cleaned_data
            form.save()
            mensaje=f'usuario "{usu}" creado correctamente'
            return render(request, "user_register.html", {'formulario':form, 'mensaje':mensaje})
        else:
            mensaje='datos invalidos'
            return render(request, "user_register.html", {'formulario':form, 'mensaje':mensaje})
    else:
        form = user_register_form()
        mensaje=""
        return render(request, "user_register.html", {'formulario':form, 'mensaje':mensaje})
    pass

def user_login(request):
    if request.method=='POST':
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            info=form.cleaned_data
            usu=info['username']
            clave=info['password']
            usuario=authenticate(username=usu, password=clave)
            if usuario != None:
                login(request, usuario)
                mensaje=f'usuario "{usu}" logueado correctamente'
                return render(request, "inicio.html", {'formulario':form, 'mensaje':mensaje})
        else:
            mensaje='datos invalidos'
            return render(request, "user_login.html", {'formulario':form, 'mensaje':mensaje})
    else:
        form=AuthenticationForm()
        mensaje=''
        return render(request, "user_login.html", {'formulario':form, 'mensaje':mensaje})

def user_perfil(request):
    pass

