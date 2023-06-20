
# Create your models here.
from django.contrib.auth.models import Group, User
from django.db import models

    
class Proveedores(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True, verbose_name='nombre')
    rubro = models.CharField(max_length=100, null=True, blank=True, verbose_name='rubro')
    email = models.EmailField(max_length=200)
    telefono = models.CharField(max_length=12)
    rut = models.IntegerField()

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre