from django.contrib import admin
from .models import Cancha
from .models import Categoria
from .models import Reserva
from .models import Insumo
# Register your models here.

admin.site.register(Cancha)
admin.site.register(Categoria)
admin.site.register(Insumo)
admin.site.register(Reserva)