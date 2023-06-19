from audioop import reverse
from django.shortcuts import render
from django.urls import reverse

# Create your views here.


import json
import pandas as pd
import xlwt
import xlwt
from django.http import HttpResponse
from django.shortcuts import redirect

#nuevas importaciones 30-05-2022
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from registration.models import Profile

#fin nuevas importaciones 30-05-2022

from django.db.models import Count, Avg, Q
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import (
	api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from ventas.models import Cliente
from ventas.models import Cotizacion
from ventas.models import DetalleCotizacion
from inventario.models import Cancha

@login_required
def ventas_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'ventas/ventas_main.html'
    return render(request,template_name,{'profile':profile})


@login_required
def gestion_cliente(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'ventas/gestion_cliente.html'
    return render(request,template_name,{'profile':profile})


# Cliente crear #

@login_required
def cliente_crear(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'ventas/cliente_crear.html'
    return render(request,template_name,{'profile':profile})

# Cliente guardar #

@login_required
def cliente_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        nombre = request.POST.get('nombre')     
        email = request.POST.get('email') 
        telefono = request.POST.get('telefono') 
        direccion = request.POST.get('direccion') 
        if nombre == '' or email == '' or telefono == '' or direccion == '':
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('cliente_crear')
        cliente_save = Cliente(
            nombre = nombre,
            email = email,
            telefono = telefono,
            direccion = direccion,
            )
        cliente_save.save()
        messages.add_message(request, messages.INFO, 'Cliente ingresado con éxito')
        return redirect('gestion_cliente')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')

# Cliente listar #


@login_required
def cliente_list(request,page=None,search=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if page == None:
        page = request.GET.get('page')
    else:
        page = page
    if request.GET.get('page') == None:
        page = page
    else:
        page = request.GET.get('page') 
    if search == None:
        search = request.GET.get('search')
    else:
        search = search
    if request.GET.get('search') == None:
        search = search
    else:
        search = request.GET.get('search') 
    if request.method == 'POST':
        search = request.POST.get('search') 
        page = None
    h_list = []
    if search == None or search == "None":
        h_count = Cliente.objects.filter().count()
        h_list_array = Cliente.objects.filter().order_by('nombre')
        for h in h_list_array:
            h_list.append({'id':h.id,'nombre':h.nombre})
    else:
        h_count = Cliente.objects.filter().filter(nombre__icontains=search).count()
        h_list_array = Cliente.objects.filter().filter(nombre__icontains=search).order_by('nombre')
        for h in h_list_array:
            h_list.append({'id':h.id,'nombre':h.nombre})            
    paginator = Paginator(h_list, 20) 
    h_list_paginate= paginator.get_page(page)   
    template_name = 'ventas/cliente_list.html'
    return render(request,template_name,{'template_name':template_name,'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page})

# Cliente ver #

@login_required
def cliente_ver(request,cliente_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    
    cliente_data = Cliente.objects.get(pk=cliente_id)
    template_name = 'ventas/cliente_ver.html'
    return render(request,template_name,{'profile':profile,'cliente_data':cliente_data})

# Cliente editar #

@login_required
def cliente_edit(request, cliente_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')

        cliente.nombre = nombre
        cliente.email = email
        cliente.telefono = telefono
        cliente.direccion = direccion
        cliente.save()

        return redirect('cliente_ver', cliente_id=cliente.id)
    else:
        cliente_data = Cliente.objects.get(pk=cliente_id)
        template_name= 'ventas/cliente_ver.html'
        return render(request, template_name, {'cliente_data': cliente_data})



# Cliente eliminar #

@login_required
def cliente_eliminar(request, cliente_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    messages.success(request, 'insumo eliminado correctamente')
    return redirect(reverse('cliente_list'))


# Cliente carga masiva #

###CARGA MASIVA PROVEEDORES####
@login_required
def cliente_carga_masiva(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'ventas/cliente_carga_masiva.html'
    return render(request,template_name,{'profiles':profiles})
@login_required
def cliente_import_file(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tienes permisos')
        return redirect('check_group_main')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="cliente_archivo_importacion.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('cliente_carga_masiva')
    row_num = 0
    columns = ['Nombre', 'Email', 'Teléfono', 'Direccón']
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/MM/yyyy'
    for row in range(1):
        row_num += 1
        for col_num in range(4):
            if col_num == 0:
                ws.write(row_num, col_num, 'Nombre', font_style)
            if col_num == 1:
                ws.write(row_num, col_num, 'Email', font_style)
            if col_num == 2:
                ws.write(row_num, col_num, 'Telefóno', font_style)
            if col_num == 3:
                ws.write(row_num, col_num, 'Dirección', font_style)
    wb.save(response)
    return response
@login_required
def cliente_carga_masiva_save(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        #try:
        print(request.FILES['myfile'])
        data = pd.read_excel(request.FILES['myfile'])
        df = pd.DataFrame(data)
        acc = 0
        for item in df.itertuples():
            #capturamos los datos desde excel
            nombre = str(item[1])
            email = str(item[2])
            telefono = int(item[3])            
            direccion = str(item[4])
            cliente_save = Cliente(
                nombre = nombre,            
                email = email,
                telefono = telefono,
                direccion = direccion,
                
                )
            cliente_save.save()
        messages.add_message(request, messages.INFO, 'Carga masiva finalizada, se importaron '+str(acc)+' registros')
        return redirect('cliente_carga_masiva')
@login_required
def generar_informe(request):
    try:
        profiles = Profile.objects.get(user_id=request.user.id)
        if profiles.group_id != 1:
            messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
            return redirect('check_group_main')

        style_1 = xlwt.easyxf('font: name Times New Roman, color-index black, bold on', num_format_str='#,##0.00')
        style_2 = xlwt.easyxf('font: name Times New Roman, color-index black, bold on')
        style_decimal = xlwt.easyxf(num_format_str='0.00')

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ReporteClientes.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Clientes')

        row_num = 0
        columns = ['Nombre', 'Email', 'Telefono','Direccion']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], style_2)

        cliente = Cliente.objects.all().order_by('nombre')
        for cliente in cliente:
            row_num += 1
            ws.write(row_num, 0, cliente.nombre, style_2)
            ws.write(row_num, 1, cliente.email, style_2)
            ws.write(row_num, 2, float(cliente.telefono), style_decimal)
            ws.write(row_num, 3, cliente.direccion, style_2)

        wb.save(response)
        return redirect('cliente_list')

    except :
        messages.add_message(request, messages.INFO, 'Error al generar el reporte')
        return redirect('cliente_list')
###Gestion de cotizacion###
@login_required
def gestion_cotizacion(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'ventas/gestion_cotizacion.html'
    return render(request,template_name,{'profile':profile})
def cotizacion_crear(request):
    cotizacion_listado= Cotizacion.objects.all()
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'ventas/cotizacion_crear.html'
    return render(request,template_name,{"cotizacion_listado":cotizacion_listado})
@login_required
def cotizacion_eliminar(request, cotizacion_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    reserva = get_object_or_404(Cotizacion, id=cotizacion_id)
    reserva.delete()
    messages.success(request, 'cotizacion eliminada correctamente')
    return redirect('cotizacion_list')
@login_required
def cotizacion_ver(request, cotizacion_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')
    cotizacion_data = Cotizacion.objects.get(pk=cotizacion_id)
    template_name = 'ventas/cotizacion_ver.html'
    return render(request, template_name, {'profile': profile, 'cotizacion_data': cotizacion_data})
@login_required
def cotizacion_save(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        fecha_creacion = request.POST.get('fecha_creacion')
        total = request.POST.get('total')
        cliente_id = request.POST.get('cliente')
        materiales = request.POST.get('materiales')
        cantidad = request.POST.get('cantidad')

        cliente = Cliente.objects.get(id=cliente_id)

        cotizacion = Cotizacion(
            nombre=nombre,
            fecha_creacion=fecha_creacion,
            total=total,
            cliente=cliente,
            materiales=materiales,
            cantidad=cantidad,
            estado='pendiente'
        )
        cotizacion.save()
        messages.add_message(request, messages.INFO, 'Cotización guardada exitosamente')
        return redirect('cotizacion_list')

    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')
@login_required
def cotizacion_list(request, page=None, search=None):
    if page is None:
        page = request.GET.get('page')
    else:
        page = page

    if request.GET.get('page') is None:
        page = page
    else:
        page = request.GET.get('page')

    if search is None:
        search = request.GET.get('search')
    else:
        search = search

    if request.GET.get('search') is None:
        search = search
    else:
        search = request.GET.get('search')
    if request.GET.get('search') is None:
        search = search
    else:
        search = request.GET.get('search')
    if request.GET.get('search') is None:
        search = search
    else:
        search = request.GET.get('search')
    

    if request.method == 'POST':
        search = request.POST.get('search')
        page = None

    cotizacion_list = []
    if search is None or search == "None":
        cotizacion_count = Cotizacion.objects.filter().count()
        cotizacion_list_array = Cotizacion.objects.all().order_by('fecha_creacion')
        for cotizacion in cotizacion_list_array:
            cotizacion_list.append({
                'id': cotizacion.id,
                'nombre': cotizacion.nombre,
                'fecha_creacion': cotizacion.fecha_creacion,
                'total': cotizacion.total,
                'cliente': cotizacion.cliente,
                'materiales': cotizacion.materiales,
                'cantidad': cotizacion.cantidad,
                'estado': cotizacion.estado
            })

    else:
        cotizacion_count = Cotizacion.objects.filter(fecha_creacion__icontains=search).count()
        cotizacion_list_array = Cotizacion.objects.filter(fecha_creacion__icontains=search).order_by('fecha_creacion')
        for cotizacion in cotizacion_list_array:
            cotizacion_list.append({
                'id': cotizacion.id,
                'nombre': cotizacion.nombre,
                'fecha_creacion': cotizacion.fecha_creacion,
                'total': cotizacion.total,
                'cliente': cotizacion.cliente,
                'materiales': cotizacion.materiales,
                'cantidad': cotizacion.cantidad,
                'estado': cotizacion.estado
            })

    paginator = Paginator(cotizacion_list, 20)
    cotizacion_list_paginate = paginator.get_page(page)

    template_name = 'ventas/cotizacion_list.html'
    return render(request, template_name, {'template_name': template_name, 'cotizacion_list_paginate': cotizacion_list_paginate, 'paginator': paginator, 'page': page})

def cotizacion_edit(request, cotizacion_id):
    if request.method == 'POST':
        cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)

        fecha_creacion = request.POST.get('fecha_creacion')
        nombre = request.POST.get('nombre')
        cliente_id = request.POST.get('cliente')
        materiales = request.POST.get('materiales')
        cantidad = request.POST.get('cantidad')
        estado = request.POST.get('estado')

        cotizacion.fecha_creacion = fecha_creacion
        cotizacion.nombre = nombre
        cotizacion.cliente_id = cliente_id
        cotizacion.materiales = materiales
        cotizacion.cantidad = cantidad
        cotizacion.estado = estado
        cotizacion.save()

        return redirect('cotizacion_ver', cotizacion_id=cotizacion.id)
    else:
        cotizacion_data = Cotizacion.objects.get(pk=cotizacion_id)
        template_name = 'ventas/cotizacion_ver.html'
        return render(request, template_name, {'cotizacion_data': cotizacion_data})

@login_required
def cotizacion_carga_masiva(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'ventas/cotizacion_carga_masiva.html'
    return render(request, template_name, {'profiles': profiles})

@login_required
def cotizacion_import_file(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tiene permisos')
        return redirect('check_group_main')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="archivo_importacion.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('cotizacion_carga_masiva')
    row_num = 0
    columns = ['Nombre', 'Descripción', 'Cantidad Disponible', 'Cantidad Utilizada']
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    for row in range(1):
        row_num += 1
        for col_num in range(4):
            if col_num == 0:
                ws.write(row_num, col_num, 'Ejemplo de nombre', font_style)
            if col_num == 1:
                ws.write(row_num, col_num, 'Ejemplo de descripción', font_style)
            if col_num == 2:
                ws.write(row_num, col_num, 10, font_style)
            if col_num == 3:
                ws.write(row_num, col_num, 5, font_style)
    wb.save(response)
    return response

@login_required
def cotizacion_carga_masiva_save(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        try:
            print(request.FILES['myfile'])
            data = pd.read_excel(request.FILES['myfile'])
            df = pd.DataFrame(data)
            count = 0
            for item in df.itertuples():
                nombre = str(item[1])
                descripcion = str(item[2])
                cantidad_disponible = int(item[3])
                cantidad_utilizada = int(item[4])
                cotizacion = Cotizacion(
                    nombre=nombre,
                    descripcion=descripcion,
                    cantidad_disponible=cantidad_disponible,
                    cantidad_utilizada=cantidad_utilizada
                )
                cotizacion.save()
                count += 1
            messages.add_message(request, messages.INFO, f'Carga masiva finalizada, se importaron {count} registros')
        except Exception as e:
            messages.add_message(request, messages.ERROR, f'Error en la carga masiva: {str(e)}')
    return redirect('cotizacion_carga_masiva')
##Detalle de la cotizacion##
def detalle_crear(request):
    cotizacion_listado= Cotizacion.objects.all()
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'ventas/detalle_crear.html'
    return render(request,template_name,{"cotizacion_listado":cotizacion_listado})
@login_required
def detalle_eliminar(request, DetalleCotizacion_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    detalle = get_object_or_404(DetalleCotizacion, id=DetalleCotizacion_id)
    detalle.delete()
    messages.success(request, 'cotizacion eliminada correctamente')
    return redirect('detalle_list')
@login_required
def detalle_ver(request, DetalleCotizacion_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')
    DetalleCotizacion_data = DetalleCotizacion.objects.get(pk=DetalleCotizacion_id)
    template_name = 'ventas/detalle_ver.html'
    return render(request, template_name, {'profile': profile, 'DetalleCotizacion_data': DetalleCotizacion_data})

@login_required
def detalle_save(request):
    if request.method == 'POST':
        cotizacion_id = request.POST.get('cotizacion')
        cancha_id = request.POST.get('cancha')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        
        cotizacion = Cotizacion.objects.get(pk=cotizacion_id)
        cancha = Cancha.objects.get(pk=cancha_id)
        
        detalle_cotizacion = DetalleCotizacion(
            cotizacion=cotizacion,
            cancha=cancha,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        detalle_cotizacion.save()
        
        messages.add_message(request, messages.INFO, 'Detalle de cotización guardado exitosamente')
        return redirect('detalle_list')
    
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')

from django.core.paginator import Paginator

@login_required
def detalle_list(request, page=None, search=None):
    if page is None:
        page = request.GET.get('page')

    if search is None:
        search = request.GET.get('search')

    if request.method == 'POST':
        search = request.POST.get('search')
        page = None

    detalle_list = []
    if search is None or search == "None":
        detalle_count = DetalleCotizacion.objects.all().count()
        detalle_list_array = DetalleCotizacion.objects.all().order_by('cancha__nombre')
        for detalle in detalle_list_array:
            detalle_list.append({'id': detalle.id, 'cancha': detalle.cancha, 'fecha_inicio': detalle.fecha_inicio, 'fecha_fin': detalle.fecha_fin, 'precio': detalle.cancha.precio})

    else:
        detalle_count = DetalleCotizacion.objects.filter(cancha__nombre__icontains=search).count()
        detalle_list_array = DetalleCotizacion.objects.filter(cancha__nombre__icontains=search).order_by('cancha__nombre')
        for detalle in detalle_list_array:
            detalle_list.append({'id': detalle.id, 'cancha': detalle.cancha, 'fecha_inicio': detalle.fecha_inicio, 'fecha_fin': detalle.fecha_fin, 'precio': detalle.cancha.precio})

    paginator = Paginator(detalle_list, 20)
    detalle_list_paginate = paginator.get_page(page)

    template_name = 'ventas/detalle_list.html'
    return render(request, template_name, {'template_name': template_name, 'detalle_list_paginate': detalle_list_paginate, 'paginator': paginator, 'page': page})


@login_required
def detalle_edit(request, detalle_id):
    detalle = get_object_or_404(DetalleCotizacion, id=detalle_id)

    if request.method == 'POST':
        cotizacion_id = request.POST.get('cotizacion_id')
        cancha_id = request.POST.get('cancha_id')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        detalle.cotizacion_id = cotizacion_id
        detalle.cancha_id = cancha_id
        detalle.fecha_inicio = fecha_inicio
        detalle.fecha_fin = fecha_fin
        detalle.save()

        return redirect('reserva_ver', detalle_id=detalle.id)
    else:
        template_name = 'ventas/detalle_ver.html'
        return render(request, template_name, {'detalle_data': detalle})

