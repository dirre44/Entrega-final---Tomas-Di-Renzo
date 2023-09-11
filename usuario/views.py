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
from django.urls import path

# Create your views here.



def obtener_avatar (request):
    if request.user.is_authenticated:
        perfil=Perfil.objects.filter(user=request.user)
        if len(perfil) != 0:
            return perfil[0].imagen.url
        else:
            return '/media/avatares/default_avatar.png' # No se porque pero a django le gusta que el default este ahi ¯\_(ツ)_/¯
    else:
        return ''

'''def obtener_avatar (request):
    if request.user.is_authenticated:
        perfil=Perfil.objects.get(user=request.user)
        if not perfil.imagen:
            return '/media/avatares/default_avatar.png' # No se porque pero a django le gusta que el default este ahi ¯\_(ツ)_/¯
        else:
            return perfil.imagen.url
    else:
        return ''
        '''


def inicio(request):
    return render(request, "inicio.html",{'avatar':obtener_avatar(request)})

def user_register (request):
    if request.method=="POST":
        form=User_register_form(request.POST)
        if form.is_valid():
            info=form.cleaned_data
            usu=info['username']
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

def user_perfil_editar(request): #No entra nunca en el if form.is_valid///pd. si no estoy logueado se rompe todo
    usuario=request.user
    perfil=Perfil.objects.get(user=usuario)
    if request.method=='POST':
        form_user=User_edit_form(request.POST)
        form_perfil=User_perfil_form(request.POST, request.FILES)
        if form_perfil.is_valid() and form_user.is_valid(): #posiblemente el problema este aca
            info_perfil=form_perfil.cleaned_data
            info_user=form_user.cleaned_data
            perfil.user=usuario
            usuario.first_name=info_user['first_name'] # lo guarda
            usuario.email=info_user['email'] # lo guarda
            usuario.password1=info_user['password1'] # lo guarda
            usuario.password2=info_user['password2'] # lo guarda
            perfil.descripcion=info_perfil['descripcion'] #lo guarda
            imagen=request.FILES['imagen']
            perfil.imagen=imagen #al fin lo guarda, era un tema en el template
            avatar_viejo=Perfil.objects.filter(user=usuario)
            if len(avatar_viejo)>0:
                avatar_viejo=avatar_viejo[0].imagen
                avatar_viejo.delete()
            perfil.save()
            usuario.save()
            #mensaje1='entra al perfil'            
            return render (request, 'user_perfil.html', {'mensaje': 'aca estoy','form_user':form_user, 'form_perfil':form_perfil, 'avatar':obtener_avatar(request), 'perfil':perfil})
        else:
            mensaje='Datos invalidos'
            return render(request, 'user_edit_perfil.html', {'form_user':form_user, 'form_perfil':form_perfil,'mensaje': mensaje}) 
    else:
        form_user=User_edit_form(instance=perfil.user)
        #form_perfil=User_perfil_form(instance=perfil)
        form_perfil=User_perfil_form(initial={'imagen':perfil.imagen, 'descripcion':perfil.descripcion}) #con el instance chillaba asi que decidi no renegar
        return render (request, 'user_edit_perfil.html', {'form_user':form_user, 'form_perfil':form_perfil, 'avatar':obtener_avatar(request), 'perfil':perfil})


def user_perfil_borrar(request):
    perfil=Perfil.objects.get(user=request.user)
    if request.method=='POST':
        perfil.delete()
        mensaje=f'Usuario {perfil.user.username} borrado'
        return render(request, "logout.html",{'avatar':obtener_avatar(request), 'mensaje':mensaje})
    pass

