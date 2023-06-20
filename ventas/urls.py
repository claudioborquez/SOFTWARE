from django.urls import path
from ventas import views
from .views import generar_informe

urlpatterns= [
    
    #Gestion de cliente
    
    path('ventas_main/',views.ventas_main,name="ventas_main"),
    
    path('gestion_cliente/',views.gestion_cliente,name="gestion_cliente"),
    
    path('cliente_carga_masiva/',views.cliente_carga_masiva,name="cliente_carga_masiva"),
    
    path('cliente_carga_masiva_save/',views.cliente_carga_masiva_save,name="cliente_carga_masiva_save"),
    
    path('cliente_import_file/',views.cliente_import_file,name="cliente_import_file"),
    
    path('cliente_crear/',views.cliente_crear,name="cliente_crear"),
    
    path('cliente_save/',views.cliente_save,name="cliente_save"),
    
    path('cliente_ver/<int:cliente_id>/',views.cliente_ver,name="cliente_ver"),
    
    path('cliente_eliminar/<int:cliente_id>/',views.cliente_eliminar,name="cliente_eliminar"),
    
    path('cliente_list/',views.cliente_list,name="cliente_list"),
    
    path('cliente_edit/<int:cliente_id>/',views.cliente_edit,name="cliente_edit"),
    ####Gestion de cotizacion###
    path('gestion_cotizacion/', views.gestion_cotizacion, name='gestion_cotizacion'),
    path('cotizacion_crear/', views.cotizacion_crear, name='cotizacion_crear'),
    path('cotizacion_eliminar/<int:cotizacion_id>/', views.cotizacion_eliminar, name='cotizacion_eliminar'),
    path('cotizacion_ver/<int:cotizacion_id>/', views.cotizacion_ver, name='cotizacion_ver'),
    path('cotizacion/save/', views.cotizacion_save, name='cotizacion_save'),
    path('cotizacion/list/', views.cotizacion_list, name='cotizacion_list'),
    path('cotizacion/edit/<int:cotizacion_id>/', views.cotizacion_edit, name='cotizacion_edit'),
    path('cotizacion/carga-masiva/', views.cotizacion_carga_masiva, name='cotizacion_carga_masiva'),
    path('cotizacion/import-file/', views.cotizacion_import_file, name='cotizacion_import_file'),
    path('cotizacion/carga-masiva/save/', views.cotizacion_carga_masiva_save, name='cotizacion_carga_masiva_save'),
    ###Detallede cotizacion###
    path('detalle_crear/', views.detalle_crear, name='detalle_crear'),
    path('detalle_eliminar/<int:DetalleCotizacion_id>/', views.detalle_eliminar, name='detalle_eliminar'),
    path('detalle_ver/<int:DetalleCotizacion_id>/', views.detalle_ver, name='detalle_ver'),
    path('detalle/save/', views.detalle_save, name='detalle_save'),
    path('detalle/list/', views.detalle_list, name='detalle_list'),
    path('detalle/edit/<int:detalle_id>/', views.detalle_edit, name='detalle_edit'),
    path('generar_informe/', generar_informe, name='generar_informe'),
    path('estado_cotizacion/<int:cotizacion_id>', views.estado_cotizacion, name= 'estado_cotizacion')

]