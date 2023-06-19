from django.contrib.auth.models import Group, User
from django.db import models
from proveedores.models import Proveedor
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio_por_hora = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return self.nombre
class Insumo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    cantidad_disponible = models.PositiveIntegerField()
    cantidad_utilizada = models.PositiveIntegerField(default=0)
    valor_insumo = models.DecimalField(max_digits=8, decimal_places=2)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
      

    def __str__(self):
        return self.nombre

    def disponible(self):
        return self.cantidad_disponible - self.cantidad_utilizada

    def agregar_utilizado(self, cantidad_disponible):
        if cantidad_disponible > self.disponible():
            raise ValueError('La cantidad utilizada supera la cantidad disponible.')
        self.cantidad_utilizada += cantidad_disponible
        self.save()

    def liberar_utilizado(self, cantidad_disponible):
        if cantidad_disponible > self.cantidad_utilizada:
            raise ValueError('La cantidad liberada supera la cantidad utilizada.')
        self.cantidad_utilizada -= cantidad_disponible
        self.save()
    def calcular_cantidad_total(self):
        return self.cantidad_utilizada * self.valor_insumo
class Cancha(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    disponible = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    insumo=models.ForeignKey(Insumo, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre
    
class Reserva(models.Model):
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    codigo = models.CharField(max_length=100)

    class Meta:
        unique_together = ('cancha', 'fecha_inicio', 'fecha_fin', 'codigo')

    def __str__(self):
        return f"{self.cancha.nombre} "

