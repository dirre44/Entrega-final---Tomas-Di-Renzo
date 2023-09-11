from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Perfil(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    imagen=models.ImageField(upload_to='avatares', null=True, blank=True)
    descripcion=models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"perfil de {self.user}"