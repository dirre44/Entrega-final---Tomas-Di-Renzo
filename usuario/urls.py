from .views import *
from django.urls import path
from django.conf.urls.static import static

app_name='app_user'
urlpatterns = [
    path('', inicio, name="usuario_inicio"),
    path('register', user_register, name="user_register"),
    path('user_login', user_login, name="user_login"),
    path("user_logout/", LogoutView.as_view(next_page='usuario_inicio'), name="user_logout"),
    path("user_perfil/", user_perfil, name='user_perfil'),
    path("user_editar_perfil/", user_perfil_editar, name='user_editar_perfil'),
    path("user_borrar_perfil/", user_perfil_borrar, name='user_borrar_perfil'),
]