from django.contrib import admin
from .models import Cliente
from .models import Cotizacion
from .models import DetalleCotizacion

admin.site.register(Cliente)
admin.site.register(Cotizacion)
admin.site.register(DetalleCotizacion)
# Register your models here.

