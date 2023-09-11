from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    titulo = models.CharField(max_length=100)
    subtitulo = models.CharField(max_length=100)
    cuerpo = models.TextField()
    fecha = models.DateField()
    imagen = models.ImageField(upload_to='avatares', null=True, blank=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'Blog de {self.autor}'
