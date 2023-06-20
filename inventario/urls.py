from django.urls import path
from inventario import views

urlpatterns= [
    ##Vistas de pagina 
    path('inventario_main/',views.inventario_main,name="inventario_main"),
    path('gestion_producto/',views.gestion_producto,name="gestion_producto"),
    path('gestion_categoria/',views.gestion_categoria,name="gestion_categoria"),
    path('gestion/material/', views.gestion_material, name='gestion_material'),
    ##
    #Gestion de producto
    path('cancha/crear/', views.cancha_crear, name='cancha_crear'),
    path('cancha/save/', views.cancha_save, name='cancha_save'),
    path('cancha/ver/<int:cancha_id>/', views.cancha_ver, name='cancha_ver'),
    path('cancha/list/', views.cancha_list, name='cancha_list'),
    path('cancha/edit/<int:cancha_id>/', views.cancha_edit, name='cancha_edit'),
    path('cancha/carga-masiva/', views.cancha_carga_masiva, name='cancha_carga_masiva'),
    path('cancha/import-file/', views.cancha_import_file, name='cancha_import_file'),
    path('cancha/carga-masiva/save/', views.cancha_carga_masiva_save, name='cancha_carga_masiva_save'),
    path('cancha/eliminar/<int:cancha_id>/', views.cancha_eliminar, name='cancha_eliminar'),
    path('generar/informe/canchas/', views.generar_informe_canchas, name='generar_informe_canchas'),
    #Gestion de categoria
    path('categoria/crear/', views.categoria_crear, name='categoria_crear'),
    path('categoria/save/', views.categoria_save, name='categoria_save'),
    path('categoria/ver/<int:categoria_id>/', views.categoria_ver, name='categoria_ver'),
    path('categoria/list/', views.categoria_list, name='categoria_list'),
    path('categoria/edit/<int:categoria_id>/', views.categoria_edit, name='categoria_edit'),
    path('categoria/carga-masiva/', views.categoria_carga_masiva, name='categoria_carga_masiva'),
    path('categoria/import-file/', views.categoria_import_file, name='categoria_import_file'),
    path('categoria/carga-masiva/save/', views.categoria_carga_masiva_save, name='categoria_carga_masiva_save'),
    path('categoria/eliminar/<int:categoria_id>/', views.categoria_eliminar, name='categoria_eliminar'),
    path('categoria/reporte/', views.generar_reporte_categorias, name='generar_reporte_categorias'),
    path('categoria/dashboard', views.categoria_dashboard, name='categoria_dashboard'),
    #Gestion de material
    path('material/crear/', views.material_crear, name='material_crear'),
    path('material/save/', views.material_save, name='material_save'),
    path('material/ver/<int:material_id>/', views.material_ver, name='material_ver'),

    path('material/list/', views.material_list, name='material_list'),
    path('material/edit/<int:material_id>/', views.material_edit, name='material_edit'),
    path('generar/informe/material/', views.generar_informe_material, name='generar_informe_material'),
    path('material/eliminar/<int:material_id>/', views.material_eliminar, name='material_eliminar'),
    ####Clase Reserva#####
    path('inventario/reserva/crear/', views.reserva_crear, name='reserva_crear'),
    path('reserva/eliminar/<int:reserva_id>/', views.reserva_eliminar, name='reserva_eliminar'),
    path('reserva/ver/<int:reserva_id>/', views.reserva_ver, name='reserva_ver'),
    path('reserva/save/', views.reserva_save, name='reserva_save'),
    path('reserva/list/', views.reserva_list, name='reserva_list'),
    path('reserva/edit/<int:reserva_id>/', views.reserva_edit, name='reserva_edit'),

]