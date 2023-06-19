
# Create your models here.
from django.contrib.auth.models import Group, User
from django.db import models

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True, verbose_name='nombre')
    rubro = models.CharField(max_length=100, null=True, blank=True, verbose_name='rubro')
    email = models.EmailField(max_length=200)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre']
    def __str__(self):
        return self.nombre
    
class Arriendo(models.Model):
    orden=models.CharField(primary_key=True,max_length=6)
    nombre=models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    producto=models.CharField(max_length=20)
    cantidad=models.PositiveSmallIntegerField()
    email = models.EmailField(max_length=200)
    
    
    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.nombre,self.cantidad)



