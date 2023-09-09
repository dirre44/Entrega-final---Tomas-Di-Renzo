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

#def obtener_avatar(request):
#    if request.user.is_authenticated:
#        avatar= Perfil.objects.filter(user=request.user.id)
#        if len(avatar) != 0:
#            return avatar[0].imagen.url
#        else:
#            return '/media/avatares/default_avatar.png'

def obtener_avatar (request):
    perfil=Perfil.objects.get(user=request.user)
    if not perfil.imagen:
        return '/media/media/avatares/default_avatar.png' # No se porque pero a django le gusta que el default este ahi ¯\_(ツ)_/¯
    else:
        return perfil.imagen.url

def inicio(request):
    return render(request, "inicio.html",{'avatar':obtener_avatar(request)})

def user_register (request):
    if request.method=="POST":
        form=User_register_form(request.POST)
        if form.is_valid():
            info=form.cleaned_data
            usu=info['username']
            info=form.cleaned_data
            form.save()                        
            mensaje=f'usuario "{usu}" creado correctamente'
            return render(request, "user_register.html", {'formulario':form, 'mensaje':mensaje, 'avatar':obtener_avatar(request)})
        else:
            mensaje='datos invalidos'
            return render(request, "user_register.html", {'formulario':form, 'mensaje':mensaje,'avatar':obtener_avatar(request)})
    else:
        form = User_register_form()
        mensaje=""
        return render(request, "user_register.html", {'formulario':form, 'mensaje':mensaje, 'avatar':obtener_avatar(request)})
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
                return render(request, "inicio.html", {'formulario':form, 'mensaje':mensaje,'avatar':obtener_avatar(request)})
        else:
            mensaje='datos invalidos'
            return render(request, "user_login.html", {'formulario':form, 'mensaje':mensaje, 'avatar':obtener_avatar(request)})
    else:
        form=AuthenticationForm()
        mensaje=''
        return render(request, "user_login.html", {'formulario':form, 'mensaje':mensaje, 'avatar':obtener_avatar(request)})

def user_perfil(request):
    perfil, created=Perfil.objects.get_or_create(user=request.user)   
    return render (request, 'user_perfil.html', {'perfil':perfil, 'avatar':obtener_avatar(request)})
    pass

def user_perfil_editar(request): #no me devuelve un http response y no se porque
    usuario=request.user
    perfil=Perfil.objects.get(user=usuario)
    if request.method=='POST':
        form_user=User_edit_form(request.POST)
        form_perfil=User_perfil_form(request.POST, request.FILES)
        if form_perfil.is_valid() and form_user.is_valid():
            info_user=form_user.cleaned_data
            info_perfil=form_perfil.cleaned_data
            perfil.user.username=info_user['username']
            perfil.user.first_name=info_user['first_name']
            perfil.user.email=info_user['email']
            perfil.user.password1=info_user['password1']
            perfil.user.password2=info_user['password2']
            perfil.descripcion=info_perfil['descripcion']
            perfil.imagen=info_perfil['imagen']
            avatar_viejo=perfil.imagen
            if len(avatar_viejo)>0:
                avatar_viejo[0].delete()
            perfil.save()
            return render (request, 'user_edit_perfil.html', {'form_user':form_user, 'form_perfil':form_perfil, 'avatar':obtener_avatar(request), 'perfil':perfil})
        pass
    else:
        form_user=User_edit_form(instance=perfil.user)
        form_perfil=User_perfil_form(initial={'imagen':perfil.imagen, 'descripcion':perfil.descripcion}) #con el instance chillaba asi que decidi no renegar
        return render (request, 'user_edit_perfil.html', {'form_user':form_user, 'form_perfil':form_perfil, 'avatar':obtener_avatar(request), 'perfil':perfil})


def user_perfil_borrar(request):
    
    pass

