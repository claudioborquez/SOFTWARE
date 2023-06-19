
#from django.conf import settings
#from django.conf.urls.static import static
#from django.contrib import admin
#from django.urls import path, include
#from core.urls import core_urlpatterns
from django.urls import path
from proveedores import views
from .views import generar_informe

urlpatterns = [
    path('generar_informe/', generar_informe, name='generar_informe'),
    path('eliminar_arriendo/<int:orden>/',views.eliminar_arriendo,name="eliminar_arriendo"),
    path('ver_arriendo/',views.ver_arriendo,name="ver_arriendo"),
    path('gestion_ver/',views.gestion_ver,name="gestion_ver"),
    path('proveedores_main/',views.proveedores_main,name="proveedores_main"),  
    #Gestion de orden de compra
    path('gestion_de_orden/',views.gestion_de_orden,name="gestion_de_orden"),
    path('arriendo_save/', views.arriendo_save, name="arriendo_save"),
    path('orden_add/',views.orden_add,name="orden_add"),
    path('orden_save/',views.orden_save,name="orden_save"),
    path('orden_ver/',views.orden_ver,name="orden_ver"),
    path('orden_list/',views.orden_list,name="orden_list"),
    path('eliminar_orden/', views.eliminar_orden, name='eliminar_orden'),
    path('orden_main/',views.orden_main,name="orden_main"),

    #Gestion de proveedores
    path('gestion_proveedores/',views.gestion_proveedores,name="gestion_proveedores"),
    path('proveedores_crear/',views.proveedores_crear,name="proveedores_crear"),
    path('proveedores_save/',views.proveedores_save,name="proveedores_save"),
    path('proveedores_ver/<int:proveedor_id>/',views.proveedores_ver,name="proveedores_ver"),
    path('proveedores_list/',views.proveedores_list,name="proveedores_list"),
    path('proveedores_edit/<int:proveedor_id>/',views.proveedores_edit,name="proveedores_edit"),
    path('proveedores_carga_masiva/',views.proveedores_carga_masiva,name="proveedores_carga_masiva"),
    path('proveedores_carga_masiva_save/',views.proveedores_carga_masiva_save,name="proveedores_carga_masiva_save"),
    path('proveedores_import_file/',views.proveedores_import_file,name="proveedores_import_file"),
    path('eliminar/<int:proveedor_id>/', views.eliminar, name='eliminar'),
    
]

#admin.site.site_header = 'Administrador Bussiness_Solutions'
#admin.site.site_title = 'bussinessSolutions'

#if settings.DEBUG:
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)