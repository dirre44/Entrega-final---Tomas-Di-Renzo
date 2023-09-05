from .views import *
from django.urls import path

urlpatterns = [
    path('', inicio, name="usuario_inicio"),

]