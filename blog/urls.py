from .views import *
from django.urls import path

urlpatterns = [
    path('', blog_mostrar_todos, name="blog_mostrar_todos"),
    path('blog_detalle/<id>', blog_mostrar_detalle, name="blog_mostrar_detalle"),
    path('blog_update/<id>', blog_update, name="blog_update"),
]