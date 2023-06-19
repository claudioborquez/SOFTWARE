from django.contrib.auth.models import Group, User
from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal


class Habilidad(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True, verbose_name='nombre')
    nivel = models.CharField(max_length=100, null=True, blank=True, verbose_name='nivel')
    hora = models.CharField(max_length=100, null=True, blank=True, verbose_name='hora')
    categoria = models.CharField(max_length=100, null=True, blank=True, verbose_name='categoria')

    estado = models.CharField(max_length=100, null=True, blank=True, default='Activo', verbose_name='Estado')   
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha Actualización')

    class Meta:
        verbose_name = 'Habilidad'
        verbose_name_plural = 'Habilidades'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Heroe(models.Model):
    habilidad = models.ForeignKey(Habilidad, on_delete=models.CASCADE)
    nombe_heroe = models.CharField(max_length=100, null=True, blank=True)
    nacionalidad_heroe = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True, default='Activo')   
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Heroe'
        verbose_name_plural = 'Heroes'
        ordering = ['nombe_heroe']
    
    def __str__(self):
        return self.nombe_heroe


def custom_upload_to(instance, filename):
    return 'product/' + filename


class Product(models.Model):
    product_name = models.CharField(max_length=100, null=True, blank=True)
    product_price = models.IntegerField(null=True, blank=True)
    product_image = models.CharField(max_length=240, null=True, blank=True)
    product_state = models.CharField(max_length=100, null=True, blank=True, default='No')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['product_name']
    
    def __str__(self):
        return self.product_name


class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    telefono = models.CharField(max_length=12)
    direccion = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Cotizacion(models.Model):
    fecha_creacion = models.DateTimeField()
    nombre = models.CharField(max_length=100)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    materiales= models.CharField(max_length=200)
    cantidad= models.DecimalField(max_digits=6, decimal_places=2)
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Cotización {self.pk} - {self.nombre}"

    class Meta:
        verbose_name = 'Cotización'
        verbose_name_plural = 'Cotizaciones'


class DetalleCotizacion(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name='detalles')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    total = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    observacion = models.TextField()

    def __str__(self):
        return f"Detalle {self.pk} - {self.cancha.nombre} - Cotización {self.cotizacion.pk}"
