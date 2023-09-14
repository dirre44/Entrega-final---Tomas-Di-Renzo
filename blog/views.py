from typing import Any, Dict
from .models import *
from .forms import * 
from usuario.models import Perfil
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
import datetime

# Create your views here.
@login_required
def blog_nuevo(request):
    if request.method=='POST':
        form=Blog_create_form(request.POST, request.FILES)
        if form.is_valid():
            blog=form.save(commit=False)
            blog.autor=request.user
            blog.save()
            return render (request, 'blog_listar.html', {'formulario':form})
        else:
            mensaje='datos invalidos'
            return render (request, 'blog_crear.html', {'formulario':form,'mensaje':mensaje})
    else:
        form=Blog_create_form()
        return render (request, 'blog_crear.html', {'formulario':form})

def blog_mostrar_detalle(request, id):
    
    blog=Blog.objects.get(id=id)
    comentarios=comentarios_leer(request,id)
    form=Blog_comentar_form()
    return render (request, 'post.html', {'blog':blog, 'comentarios':comentarios, 'formulario':form})
    # mostrar el blog en los template --listo--
    pass

def blog_mostrar_todos(request):
    
    lista_blog=Blog.objects.all()
    return render (request, 'blog_listar.html', {'lista_blog':lista_blog})
    # Mostrar cada blog en un FOR en los template --listo--

@login_required
def blog_update(request, id):
    blog=get_object_or_404(Blog, id=id)
    # es importante que el unico que pueda editar sea el autor y el admin  --listo--
    if request.user == blog.autor or request.user.is_staff:
        if request.method=='POST':
            form=Blog_create_form(request.POST, request.FILES, instance=blog)
            if form.is_valid():
                form.save()
                return render (request, 'blog_listar.html', {'formulario':form, 'blog':blog})
            else:
                mensaje='datos invalidos'
                return render (request, 'blog_editar.html', {'formulario':form,'mensaje':mensaje, 'blog':blog})
        else:
            form=Blog_create_form(instance=blog)
            return render (request, 'blog_editar.html', {'formulario':form, 'blog':blog})
    else:
        return redirect('app_blog:blog_mostrar_todos')

@login_required
def blog_eliminar(request, id):
    blog=get_object_or_404(Blog, id=id)
    if request.user == blog.autor or request.user.is_staff:
        if request.method=='POST':
            blog.delete()
            return redirect('app_blog:blog_mostrar_todos')
        else:
            return render(request, 'blog_eliminar.html', {'blog':blog})
    else:
        return HttpResponseForbidden("No tienes permiso para editar este blog.")
            
    pass


def comentarios_leer(request, id):
    receptor=Blog.objects.get(id=id)
    comentarios=Comentario.objects.filter(receptor=receptor)
    return comentarios

@login_required
def blog_comentar(request, id):
    if request.method=='POST':
        form=Blog_comentar_form(request.POST)
        if form.is_valid():
            comentario=form.save(commit=False)
            comentario.autor=request.user
            receptor=Blog.objects.get(id=id)
            comentario.receptor=receptor
            comentario.save()
            return redirect('app_blog:blog_mostrar_detalle', id=id)
        else:
            return redirect('app_blog:blog_mostrar_detalle', id=id)
    else:
        return redirect('app_blog:blog_mostrar_todos')
