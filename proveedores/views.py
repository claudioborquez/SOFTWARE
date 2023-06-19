import json
import pandas as pd
import xlwt
#nuevas importaciones 30-05-2022
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from registration.models import Profile

from django.db.models import Count, Avg, Q
from django.shortcuts import render, redirect
from rest_framework import generics, viewsets
from rest_framework.decorators import (
	api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse, reverse_lazy
from .models import Arriendo
from .models import Proveedor
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

@login_required
def proveedores_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedores/proveedores_main.html'
    return render(request,template_name,{'profile':profile})

@login_required
def gestion_proveedores(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedores/gestion_proveedores.html'
    return render(request,template_name,{'profile':profile})
@login_required
def orden_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedores/orden_main.html'
    return render(request,template_name,{'profile':profile})
@login_required
def gestion_de_orden(request):
    arriendosListados= Arriendo.objects.all()
    proveedores_listado= Proveedor.objects.all()
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedores/gestion_de_orden.html'
    return render(request,template_name,{"arriendos": arriendosListados, "proveedores_listado": proveedores_listado})

    
@login_required
def gestion_ver(request):
    arriendosListados= Arriendo.objects.all()
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedores/gestion_ver.html'
    return render(request,template_name,{"arriendos": arriendosListados})


@login_required
def arriendo_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        orden = request.POST.get('orden')
        producto = request.POST.get('producto')
        cantidad = request.POST.get('cantidad')
        email = request.POST.get('email')

        if nombre == '' or orden == '' or producto == '' or cantidad == '' or email == '':
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('gestion_de_orden')
        proveedor_nombre=Proveedor.objects.get (id=nombre)
        
        arriendo_save = Arriendo(
            nombre = proveedor_nombre,
            producto = producto,
            orden = orden,
            cantidad = cantidad,
            email = email,
            )
        arriendo_save.save()
        
        return redirect('gestion_de_orden')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')
    





######################################################################################
#Crud orden de compra
@login_required
def orden_add(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedores/orden_add.html'
    return render(request,template_name,{'profile':profile})
@login_required
def orden_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        nivel = request.POST.get('nivel')
        hora = request.POST.get('hora')        
        if nombre == '' or nivel == '':
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('orden_add')
        orden_save = Proveedor(
            nombre = nombre,
            nivel = nivel,
            hora = hora,
            )
        orden_save.save()
        messages.add_message(request, messages.INFO, 'Orden ingresada con éxito')
        return redirect('orden_list')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')
    
@login_required    
def eliminar_arriendo(request, orden ):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    orden = get_object_or_404(Arriendo, orden=orden)
    orden.delete()
    
    return redirect(reverse('gestion_ver'))



@login_required
def ver_arriendo(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tienes permisos')
        return redirect('check_group_main')

    page = request.GET.get('page', 1)
    search = request.GET.get('search', '')

    if request.method == 'POST':
        search = request.POST.get('search')
        page = None

    if search:
        try:
            search_int = int(search)
            arriendosListados = Arriendo.objects.filter(
                Q(orden__icontains=search) |
                Q(cantidad=search_int) |
                Q(producto__icontains=search) |
                Q(email__icontains=search)  # Incluye el campo email en la búsqueda
            )
        except ValueError:
            arriendosListados = Arriendo.objects.filter(
                Q(orden__icontains=search) |
                Q(nombre__nombre__icontains=search) |
                Q(producto__icontains=search) |
                Q(email__icontains=search)  # Incluye el campo email en la búsqueda
            )
    else:
        arriendosListados = Arriendo.objects.all()

    gestion_ver = []
    for arriendo in arriendosListados:
        gestion_ver.append({
            'orden': arriendo.orden,
            'nombre': arriendo.nombre,
            'producto': arriendo.producto,
            'cantidad': arriendo.cantidad,
            'email': arriendo.email,
        })

    paginator = Paginator(gestion_ver, 20)
    gestion_ver_paginate = paginator.get_page(page)

    template_name = 'proveedores/gestion_ver.html'
    return render(request, template_name, {
        'template_name': template_name,
        'arriendos': arriendosListados,
        'gestion_ver_paginate': gestion_ver_paginate,
        'paginator': paginator,
        'page': page,
    })



#eliminar
@login_required
def orden_ver(request,Proveedor_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    Proveedor_data = Proveedor.objects.get(pk=Proveedor_id)
    template_name = 'proveedores/orden_ver.html'
    return render(request,template_name,{'profile':profile,'Proveedor_data':Proveedor_data})

@login_required
def eliminar_orden(request, Proveedor_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    Proveedor = get_object_or_404(Proveedor, id=Proveedor_id)
    Proveedor.delete()
    messages.success(request, 'Orden eliminada correctamente')
    return redirect(reverse('orden_ver'))
@login_required
def orden_list(request, page=None, search=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

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

    if request.method == 'POST':
        search = request.POST.get('search')
        page = None

    h_list = []
    if search is None or search == "None":
        h_count = Proveedor.objects.count()
        h_list_array = Proveedor.objects.order_by('nivel')
        for h in h_list_array:
            h_list.append({'id': h.id, 'nombre': h.nombre, 'nivel': h.nivel, 'hora': h.hora})
    else:
        h_count = Proveedor.objects.filter(nombre__icontains=search).count()
        h_list_array = Proveedor.objects.filter(nombre__icontains=search).order_by('nombre')
        for h in h_list_array:
            h_list.append({'id': h.id, 'nombre': h.nombre, 'nivel': h.nivel, 'hora': h.hora})

    paginator = Paginator(h_list, 20)
    h_list_paginate = paginator.get_page(page)
    template_name = 'proveedores/orden_list.html'
    return render(request, template_name, {'template_name': template_name, 'h_list_paginate': h_list_paginate, 'paginator': paginator, 'page': page})
@login_required
def orden_Proveedor_edit(request, Proveedor_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    Proveedor = get_object_or_404(Proveedor, id=Proveedor_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        nivel = request.POST.get('nivel')
        hora = request.POST.get('hora')

        Proveedor.nombre = nombre
        Proveedor.nivel = nivel
        Proveedor.hora = hora
        Proveedor.save()

        return redirect('orden_ver', Proveedor_id=Proveedor.id)
    else:
        Proveedor_data = Proveedor.objects.get(pk=Proveedor_id)
        template_name= 'proveedores/proveedores_ver.html'
        return render(request, template_name, {'Proveedor_data': Proveedor_data})
##################################################################################
#CRUD DE PROVEEDORES
@login_required
def proveedores_crear(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedores/proveedores_crear.html'
    return render(request,template_name,{'profile':profile})

@login_required
def proveedores_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tienes permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        rubro = request.POST.get('rubro')
        email = request.POST.get('email')
        if nombre == '' or rubro == '' or email == '':
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('proveedores_crear')
        proveedor_save = Proveedor(
            nombre=nombre,
            rubro=rubro,
            email=email,
        )
        proveedor_save.save()
        messages.add_message(request, messages.INFO, 'Proveedor ingresado con éxito')
        return redirect('proveedores_list')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')


@login_required
def proveedores_ver(request,proveedor_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    proveedor_data = Proveedor.objects.get(pk=proveedor_id)
    template_name = 'proveedores/proveedores_ver.html'
    return render(request,template_name,{'profile':profile,'proveedor_data':proveedor_data})
@login_required
def proveedores_list(request, page=None, search=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')
    
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
    
    if request.method == 'POST':
        search = request.POST.get('search')
        page = None
    
    h_list = []
    
    if search is None or search == "None":
        h_count = Proveedor.objects.count()
        h_list_array = Proveedor.objects.order_by('rubro')
        for h in h_list_array:
            h_list.append({'id': h.id, 'nombre': h.nombre, 'rubro': h.rubro})
    else:
        h_count = Proveedor.objects.filter(nombre__icontains=search).count()
        h_list_array = Proveedor.objects.filter(nombre__icontains=search).order_by('nombre')
        for h in h_list_array:
            h_list.append({'id': h.id, 'nombre': h.nombre, 'rubro': h.rubro})
    
    paginator = Paginator(h_list, 20)
    h_list_paginate = paginator.get_page(page)
    template_name = 'proveedores/proveedores_list.html'
    
    return render(request, template_name, {'template_name': template_name, 'h_list_paginate': h_list_paginate, 'paginator': paginator, 'page': page})
@login_required
def proveedores_edit(request, proveedor_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        rubro = request.POST.get('rubro')
        email= request.POST.get('email')

        proveedor.nombre = nombre
        proveedor.rubro = rubro
        proveedor.email = email
        proveedor.save()

        return redirect('proveedores_ver', proveedor_id=proveedor.id)
    else:
        proveedor_data = Proveedor.objects.get(pk=proveedor_id)
        template_name= 'proveedores/proveedores_ver.html'
        return render(request, template_name, {'proveedor_data': proveedor_data})
@login_required
def eliminar(request, proveedor_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    proveedor.delete()
    messages.success(request, 'Proveedor eliminado correctamente')
    return redirect(reverse('proveedores_list'))
###CARGA MASIVA PROVEEDORES####
@login_required
def proveedores_carga_masiva(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedores/proveedores_carga_masiva.html'
    return render(request,template_name,{'profiles':profiles})
@login_required
def proveedores_import_file(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tiene permisos')
        return redirect('check_group_main')
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="archivo_importacion.xls"'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('proveedores_carga_masiva')
    row_num = 0
    columns = ['Tipo de proveedor', 'Nivel', 'Email']
    
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/MM/yyyy'
    
    for row in range(1):
        row_num += 1
        for col_num in range(3):
            if col_num == 0:
                ws.write(row_num, col_num, 'ej: habilidad', font_style)
            if col_num == 1:
                ws.write(row_num, col_num, '88', font_style)
            if col_num == 2:
                ws.write(row_num, col_num, 'example@example.com', font_style)
    
    wb.save(response)
    return response


@login_required
def proveedores_carga_masiva_save(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tiene permisos')
        return redirect('check_group_main')
    
    if request.method == 'POST':
        # try:
        print(request.FILES['myfile'])
        data = pd.read_excel(request.FILES['myfile'])
        df = pd.DataFrame(data)
        acc = 0
        
        for item in df.itertuples():
            # Capturamos los datos desde Excel
            nombre = str(item[1])            
            nivel = int(item[2])
            email = str(item[3])
            
            proveedor_save = Proveedor(
                nombre=nombre,            
                rubro=nivel,
                email=email,
            )
            proveedor_save.save()
            acc += 1
        
        messages.add_message(request, messages.INFO, 'Carga masiva finalizada, se importaron ' + str(acc) + ' registros')
        return redirect('proveedores_carga_masiva')
    
@login_required
def generar_informe(request):
    filtro_orden = request.GET.get('filtro_orden', '')
    filtro_nombre = request.GET.get('filtro_nombre', '')
    filtro_producto = request.GET.get('filtro_producto', '')
    filtro_cantidad = request.GET.get('filtro_cantidad', '')
    filtro_email = request.GET.get('filtro_email', '')  # Nuevo filtro por email

    arriendos = Arriendo.objects.all()

    if filtro_orden:
        arriendos = arriendos.filter(orden__icontains=filtro_orden)

    if filtro_nombre:
        arriendos = arriendos.filter(nombre__nombre__icontains=filtro_nombre)

    if filtro_producto:
        arriendos = arriendos.filter(producto__icontains=filtro_producto)

    if filtro_cantidad:
        try:
            cantidad = int(filtro_cantidad)
            arriendos = arriendos.filter(cantidad=cantidad)
        except ValueError:
            pass

    if filtro_email:
        arriendos = arriendos.filter(email__icontains=filtro_email)  # Filtrar por email

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="informe.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)

    data = [['Orden', 'Nombre', 'Producto', 'Cantidad', 'Email']]

    for arriendo in arriendos:
        data.append([
            arriendo.orden,
            arriendo.nombre.nombre,
            arriendo.producto,
            arriendo.cantidad,
            arriendo.email,
        ])

    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    table = Table(data)
    table.setStyle(table_style)

    elements = [table]
    doc.build(elements)

    return response
