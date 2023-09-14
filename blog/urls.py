from .views import *
from django.urls import path

app_name='app_blog'
urlpatterns = [
    path('', blog_mostrar_todos, name="blog_mostrar_todos"),
    path('blog_detalle/<id>', blog_mostrar_detalle, name="blog_mostrar_detalle"),
    path('blog_update/<id>', blog_update, name="blog_update"),
    path('blog_crear', blog_nuevo, name="blog_crear"),
    path('blog_editar/<id>', blog_update, name="blog_editar"),
    path('blog_comentar/<id>', blog_comentar, name="blog_comentar"),
    path('blog_eliminar/<id>', blog_eliminar, name="blog_eliminar"),
]