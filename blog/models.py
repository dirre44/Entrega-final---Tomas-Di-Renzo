from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    titulo = models.CharField(max_length=100)
    subtitulo = models.CharField(max_length=100)
    cuerpo = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    imagen = models.ImageField(upload_to='avatares', null=True, blank=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.titulo} - {self.autor}'
    
class Comentario(models.Model):
    autor=models.ForeignKey(User, on_delete=models.CASCADE)
    receptor=models.ForeignKey(Blog, on_delete=models.CASCADE)
    cuerpo = models.TextField()
    def __str__(self):
        return f'comentario de {self.autor} en {self.receptor}'