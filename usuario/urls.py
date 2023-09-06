from .views import *
from django.urls import path

urlpatterns = [
    path('', inicio, name="usuario_inicio"),
    path('register', user_register, name="user_register"),
    path('user_login', user_login, name="user_login"),
    path("user_logout/", LogoutView.as_view(next_page='inicio'), name="logout"),
    path("user_perfil/", user_perfil, name='user_perfil')
]