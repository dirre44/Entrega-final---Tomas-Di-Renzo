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
import datetime

# Create your views here.

def blog_nuevo(request):
    if request.method=='POST':
        form=Blog_create_form(request.POST, request.FILES)
        if form.is_valid():
            blog=form.save(commit=False)
            blog.fecha=datetime.date.today
            blog.autor=request.user
            blog.save()
        else:
            pass
    else:
        form=Blog_create_form()

def blog_mostrar_detalle(request, id):
    blog=Blog.objects.get(id=id)
    # mostrar el blog en los template
    pass

def blog_mostrar_todos(request):
    lista_blog=Blog.objects.all()
    return render (request, 'blog_listar.html', {'lista_blog':lista_blog})
    # Mostrar cada blog en un FOR en los template

def blog_update(request, id):
    # es importante que el unico que pueda editar sea el autor
    blog=Blog.objects.get(id=id)
    if request.method=='POST':
        form=Blog_create_form(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
        else:
            mensaje='datos invalidos'
    else:
        form=Blog_create_form(instance=blog)

    pass

def blog_borrar(request, id):

    pass

