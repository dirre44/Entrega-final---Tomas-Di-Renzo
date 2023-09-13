from typing import Any, Dict
from .models import *
from .forms import * 
from django.shortcuts import render, redirect
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
import datetime

# Create your views here.

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
    return render (request, 'post.html', {'blog':blog, 'comentarios':comentarios})
    # mostrar el blog en los template --listo--
    pass

def blog_mostrar_todos(request):
    form=Blog_comentar_form()
    lista_blog=Blog.objects.all()
    return render (request, 'blog_listar.html', {'lista_blog':lista_blog, 'formulario':form})
    # Mostrar cada blog en un FOR en los template --listo--

def blog_update(request, id):
    # es importante que el unico que pueda editar sea el autor
    blog=Blog.objects.get(id=id)
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


def blog_borrar(request, id):

    pass


def comentarios_leer(request, id):
    comentarios=Comentario.objects.filter(receptor=id)
    return comentarios

def blog_comentar(request, id):
    if request.method=='POST':
        form=Blog_comentar_form(request.POST)
        if form.is_valid():
            comentario=form.save(commit=False)
            comentario.autor=request.user
            comentario.receptor=id
            comentario.save()
            return redirect('blog_mostrar_detalle', id=id)
        else:
            return redirect('blog_mostrar_detalle', id=id)
    else:
        return redirect('blog_mostrar_todos')
    pass

