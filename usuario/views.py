from typing import Any, Dict
from .models import *
from .forms import * 
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
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
def inicio(request):
    return render(request, "inicio.html")

def user_register (request):
    if request.method=="POST":
        form=User_register_form(request.POST)
        if form.is_valid():
            info=form.cleaned_data
            usu=info['username']
            form.save()                    
            mensaje=f'usuario "{usu}" creado correctamente'
            return render(request, "user_register.html", {'formulario':form, 'mensaje':mensaje})
        else:
            mensaje='datos invalidos'
            return render(request, "user_register.html", {'formulario':form, 'mensaje':mensaje})
    else:
        form = User_register_form()
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

def user_perfil(request, user_id=None): #muestra mi perfil o muestra un perfil un perfil pedido
    if user_id is None:
        user = request.user
    else:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect('app_blog:blog_mostrar_todos')    
    perfil, created = Perfil.objects.get_or_create(user=user)
    if created==True:
        perfil.imagen = '/media/avatares/default_avatar.png' 
        perfil.save()    
    return render(request, 'user_perfil.html', {'perfil': perfil})


@login_required
def user_perfil_editar(request): #No entra nunca en el if form.is_valid///pd. si no estoy logueado se rompe todo
    usuario=request.user
    perfil=Perfil.objects.get(user=usuario)
    # if request.user.is_staff or perfil.user==request.user: HACE FALTA ESTO??
    if request.method=='POST':
        form_user=User_edit_form(request.POST, instance=usuario)
        form_perfil=User_perfil_form(request.POST, request.FILES, instance=perfil)
        if form_perfil.is_valid() and form_user.is_valid(): #posiblemente el problema este aca
            form_user.save()
            form_perfil.save()
            usuario=authenticate(
                username=request.user.username,
                password=form_user.cleaned_data['password1'])      
            if usuario is not None:
                login(request, usuario)

            return render (request, 'user_perfil.html', {'form_user':form_user, 'form_perfil':form_perfil, 'perfil':perfil})
        else:
            mensaje='Datos invalidos'
            return render(request, 'user_edit_perfil.html', {'form_user':form_user, 'form_perfil':form_perfil,'mensaje': mensaje}) 
    else:
        form_user=User_edit_form(instance=perfil.user)
        # form_perfil=User_perfil_form(instance=perfil)
        form_perfil=User_perfil_form(initial={'imagen':perfil.imagen, 'descripcion':perfil.descripcion}) #con el instance chillaba asi que decidi no renegar
        return render (request, 'user_edit_perfil.html', {'form_user':form_user, 'form_perfil':form_perfil,  'perfil':perfil})
    

            # info_perfil=form_perfil.cleaned_data
            # info_user=form_user.cleaned_data
            # perfil.user=usuario
            # usuario.first_name=info_user['first_name'] # lo guarda
            # usuario.email=info_user['email'] # lo guarda
            # usuario.password1=info_user['password1'] # lo guarda
            # usuario.password2=info_user['password2'] # lo guarda
            # perfil.descripcion=info_perfil['descripcion'] #lo guarda
            # imagen=request.FILES['imagen']
            # perfil.imagen=imagen #al fin lo guarda, era un tema en el template
            # avatar_viejo=Perfil.objects.filter(user=usuario)
            # if len(avatar_viejo)>0:
            #     avatar_viejo=avatar_viejo[0].imagen
            #     avatar_viejo.delete()


@login_required
def user_perfil_borrar(request):
    perfil=get_object_or_404(Perfil, user=request.user)
    if request.user == perfil.user or request.user.is_staff:
        if request.method=='POST':
            perfil.delete()
            return redirect('app_user:usuario_inicio')
        else:
            return render(request, 'perfil_eliminar.html', { 'perfil':perfil})
    else:
        return HttpResponseForbidden("No tienes permiso para editar este blog.")
    pass

