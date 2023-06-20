from audioop import reverse
from django.shortcuts import render

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
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from django.shortcuts import render
from collections import Counter

#fin nuevas importaciones 30-05-2022

from django.db.models import Count, Avg, Q
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import (
	api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from inventario.models import Categoria
from inventario.models import Cancha
from inventario.models import Material
from inventario.models import Reserva
from proveedores.models import Proveedor
###Vista de app , producto , categoria , material
@login_required
def inventario_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'inventario/inventario_main.html'
    return render(request,template_name,{'profile':profile})

@login_required
def gestion_producto(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'inventario/gestion_producto.html'
    return render(request,template_name,{'profile':profile})

@login_required
def gestion_categoria(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'inventario/gestion_categoria.html'
    return render(request,template_name,{'profile':profile})
@login_required
def gestion_material(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'inventario/gestion_material.html'
    return render(request,template_name,{'profile':profile})
#CRUD PARA PRODUCTO
@login_required
def cancha_crear(request):
    categoria_listado= Categoria.objects.all()
    material_listado= material.objects.all()
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tienes permisos')
        return redirect('check_group_main')
    template_name = 'inventario/cancha_crear.html'
    return render(request, template_name, {'profile': profile,'categoria_listado':categoria_listado,'material_listado':material_listado})

def cancha_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tienes permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        ubicacion = request.POST.get('ubicacion')
        disponible = request.POST.get('disponible')
        categoria_id = request.POST.get('categoria')
        material_id = request.POST.get('material')

        if not nombre or not ubicacion or not disponible or not categoria_id or not material_id:
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('cancha_crear')

        categoria1 = Categoria.objects.get(id=categoria_id)
        material1 = material.objects.get(id=material_id)
        cancha_save = Cancha(
            nombre=nombre,
            ubicacion=ubicacion,
            disponible=bool(disponible),
            categoria=categoria1,
            material=material1,
        )
        cancha_save.save()
        messages.add_message(request, messages.INFO, 'Cancha ingresada con éxito')
        return redirect('cancha_crear')

    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')



@login_required
def cancha_ver(request, cancha_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tienes permisos')
        return redirect('check_group_main')

    cancha_data = Cancha.objects.get(pk=cancha_id)
    template_name = 'inventario/cancha_ver.html'
    return render(request, template_name, {'profile': profile, 'cancha_data': cancha_data})
@login_required
def cancha_list(request, page=None, search=None):
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

    cancha_list = []
    if search is None or search == "None":
        cancha_count = Cancha.objects.filter().count()
        cancha_list_array = Cancha.objects.all().order_by('nombre')
        for cancha in cancha_list_array:
            cancha_list.append({
                'id': cancha.id,
                'nombre': cancha.nombre,
                'ubicacion': cancha.ubicacion,
                'disponible': cancha.disponible,
                'categoria': cancha.categoria,
                'material': cancha.material
            })
            
    else:
        cancha_count = Cancha.objects.filter(nombre__icontains=search).count()
        cancha_list_array = Cancha.objects.filter(nombre__icontains=search).order_by('nombre')
        for cancha in cancha_list_array:
            cancha_list.append({
                'id': cancha.id,
                'nombre': cancha.nombre,
                'ubicacion': cancha.ubicacion,
                'disponible': cancha.disponible,
                'categoria': cancha.categoria,
                'material': cancha.material
            })


    paginator = Paginator(cancha_list, 20)
    cancha_list_paginate = paginator.get_page(page)

    template_name = 'inventario/cancha_list.html'
    return render(request, template_name, {'template_name': template_name, 'cancha_list_paginate': cancha_list_paginate, 'paginator': paginator, 'page': page})


@login_required
def cancha_edit(request, cancha_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tienes permisos')
        return redirect('check_group_main')

    cancha = get_object_or_404(Cancha, id=cancha_id)

    if request.method == 'POST':
        cancha_nombre = request.POST.get('nombre')
        cancha_ubicacion = request.POST.get('ubicacion')
        cancha_disponible = request.POST.get('disponible')

        cancha.nombre = cancha_nombre
        cancha.ubicacion = cancha_ubicacion
        cancha.disponible = cancha_disponible
        cancha.save()

        return redirect('cancha_ver', cancha_id=cancha.id)
    else:
        cancha_data = Cancha.objects.get(pk=cancha_id)
        template_name = 'inventario/cancha_ver.html'
        return render(request, template_name, {'cancha_data': cancha_data})



@login_required
def cancha_carga_masiva(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tienes permisos')
        return redirect('check_group_main')
    template_name = 'inventario/cancha_carga_masiva.html'
    return render(request, template_name, {'profiles': profiles})


@login_required
def cancha_import_file(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tienes permisos')
        return redirect('check_group_main')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="archivo_importacion.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('cancha_carga_masiva')
    row_num = 0
    columns = ['Nombre', 'Descripción', 'Precio por Hora']
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
                ws.write(row_num, col_num, 'Ejemplo de nombre', font_style)
            if col_num == 1:
                ws.write(row_num, col_num, 'Ejemplo de descripción', font_style)
            if col_num == 2:
                ws.write(row_num, col_num, '99.99', font_style)
    wb.save(response)
    return response
@login_required
def cancha_carga_masiva_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tienes permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        try:
            file = request.FILES['myfile']
            df = pd.read_excel(file)
            count = 0
            for row in df.itertuples():
                nombre = str(row[1])
                descripcion = str(row[2])
                precio_por_hora = float(row[3])
                cancha = Cancha(
                    nombre=nombre,
                    descripcion=descripcion,
                    precio_por_hora=precio_por_hora
                )
                cancha.save()
                count += 1
            messages.success(request, f'Se han importado {count} registros exitosamente.')
        except Exception as e:
            messages.error(request, f'Error en la carga masiva: {str(e)}')

    return redirect('cancha_list')
@login_required
def cancha_eliminar(request, cancha_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    cancha = get_object_or_404(Cancha, id=cancha_id)
    cancha.delete()
    messages.success(request, 'Categoria eliminado correctamente')
    return redirect('cancha_list')
@login_required
def generar_informe_canchas(request):
    filtro_nombre = request.GET.get('filtro_nombre', '')
    filtro_disponible = request.GET.get('filtro_disponible', '')
    filtro_ubicacion= request.GET.get('filtro_ubicacion', '')

    canchas = Cancha.objects.all()

    if filtro_nombre:
        canchas = canchas.filter(nombre__icontains=filtro_nombre)

    if filtro_disponible:
        try:
            disponible = int(filtro_disponible)
            canchas = canchas.filter(disponible=disponible)
        except ValueError:
            pass

    if filtro_ubicacion:
        try:
            utilizada = int(filtro_ubicacion)
            canchas = canchas.filter(cantidad_utilizada=utilizada)
        except ValueError:
            pass

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="informe.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)

    data = [['Nombre', 'Ubicación', 'Disponible']]

    for cancha in canchas:
        data.append([
            cancha.nombre,
            cancha.ubicacion,
            str(cancha.disponible),
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

#CRUD PARA CATEGORIA 

def categoria_crear(request):
    categoria_listado= Categoria.objects.all()
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'inventario/categoria_crear.html'
    return render(request,template_name,{"categoria_listado":categoria_listado})


@login_required
def categoria_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio_por_hora = request.POST.get('precio_por_hora')

        if not nombre or not descripcion or not precio_por_hora:
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('categoria_crear')

        categoria = Categoria(
            nombre=nombre,
            descripcion=descripcion,
            precio_por_hora=precio_por_hora
        )
        categoria.save()
        messages.add_message(request, messages.INFO, 'Categoría ingresada con éxito')
        return redirect('categoria_list')
    
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')

@login_required
def categoria_ver(request, categoria_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')

    categoria_data = Categoria.objects.get(pk=categoria_id)
    template_name = 'inventario/categoria_ver.html'
    return render(request, template_name, {'profile': profile, 'categoria_data': categoria_data})


@login_required
def categoria_list(request, page=None, search=None):
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

    categoria_list = []
    if search is None or search == "None":
        categoria_count = Categoria.objects.filter().count()
        categoria_list_array = Categoria.objects.all().order_by('nombre')
        for categoria in categoria_list_array:
            categoria_list.append({'id': categoria.id, 'nombre': categoria.nombre,'descricion':categoria.descripcion,'precio_por_hora':categoria.precio_por_hora})
            
    else:
        categoria_count = Categoria.objects.filter(nombre__icontains=search).count()
        categoria_list_array = Categoria.objects.filter(nombre__icontains=search).order_by('nombre')
        for categoria in categoria_list_array:
            categoria_list.append({'id': categoria.id, 'nombre': categoria.nombre,'descricion':categoria.descripcion,'precio_por_hora':categoria.precio_por_hora})


    paginator = Paginator(categoria_list, 20)
    categoria_list_paginate = paginator.get_page(page)

    template_name = 'inventario/categoria_list.html'
    return render(request, template_name, {'template_name': template_name, 'categoria_list_paginate': categoria_list_paginate, 'paginator': paginator, 'page': page})


@login_required
def categoria_edit(request, categoria_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')

    categoria = get_object_or_404(Categoria, id=categoria_id)

    if request.method == 'POST':
        categoria_nombre = request.POST.get('categoria')

        if categoria_nombre:
            categoria.nombre = categoria_nombre
            categoria.save()
            return redirect('categoria_ver', categoria_id=categoria.id)
        else:
            messages.error(request, 'El nombre de categoría no puede estar vacío')
            # En lugar de redirigir a 'categoria_edit', redirige a 'categoria_ver' con el mismo 'categoria_id'
            return redirect('categoria_ver', categoria_id=categoria.id)
    else:
        categoria_data = Categoria.objects.get(pk=categoria_id)
        template_name = 'inventario/categoria_ver.html'
        return render(request, template_name, {'categoria_data': categoria_data})
@login_required
def generar_reporte_categorias(request):
    try:
        profiles = Profile.objects.get(user_id=request.user.id)
        if profiles.group_id != 1:
            messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
            return redirect('check_group_main')

        style_1 = xlwt.easyxf('font: name Times New Roman, color-index black, bold on', num_format_str='#,##0.00')
        style_2 = xlwt.easyxf('font: name Times New Roman, color-index black, bold on')
        style_decimal = xlwt.easyxf(num_format_str='0.00')

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ReporteCategorias.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Categorías')

        row_num = 0
        columns = ['Nombre', 'Descripción', 'Precio por Hora']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], style_2)

        categorias = Categoria.objects.all().order_by('nombre')
        for categoria in categorias:
            row_num += 1
            ws.write(row_num, 0, categoria.nombre, style_2)
            ws.write(row_num, 1, categoria.descripcion, style_2)
            ws.write(row_num, 2, float(categoria.precio_por_hora), style_decimal)

        wb.save(response)
        return redirect('categoria_list')

    except :
        messages.add_message(request, messages.INFO, 'Error al generar el reporte')
        return redirect('categoria_list')

@login_required
def categoria_carga_masiva(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'inventario/categoria_carga_masiva.html'
    return render(request, template_name, {'profiles': profiles})

@login_required
def categoria_import_file(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="archivo_importacion.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('categoria_carga_masiva')
    row_num = 0
    columns = ['Nombre', 'Descripción', 'Precio por Hora']
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
                ws.write(row_num, col_num, 'Ejemplo de nombre', font_style)
            if col_num == 1:
                ws.write(row_num, col_num, 'Ejemplo de descripción', font_style)
            if col_num == 2:
                ws.write(row_num, col_num, '99.99', font_style)
    wb.save(response)
    return response

@login_required
def categoria_carga_masiva_save(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
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
                precio_por_hora = float(item[3])
                categoria = Categoria(
                    nombre=nombre,
                    descripcion=descripcion,
                    precio_por_hora=precio_por_hora
                )
                categoria.save()
                count += 1
            messages.add_message(request, messages.INFO, f'Carga masiva finalizada, se importaron {count} registros')
        except Exception as e:
            messages.add_message(request, messages.ERROR, f'Error en la carga masiva: {str(e)}')
    return redirect('categoria_carga_masiva')
@login_required
def categoria_eliminar(request, categoria_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    categoria = get_object_or_404(Categoria, id=categoria_id)
    categoria.delete()
    messages.success(request, 'Categoria eliminado correctamente')
    return redirect('categoria_list')

def categoria_dashboard(request):
    categorias = Categoria.objects.all()
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')

    total_categorias = len(categorias)
    categorias_counter = Counter(categoria.nombre for categoria in categorias)
    porcentajes = [(nombre, (count / total_categorias) * 100) for nombre, count in categorias_counter.items()]

    template_name = 'inventario/gestion_categoria.html'
    return render(request, template_name, {'categorias': categorias, 'porcentajes': porcentajes})


#CRUD PARA materials

@login_required
def material_crear(request):
    proveedores_listado= Proveedor.objects.all()
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'inventario/material_crear.html'
    return render(request,template_name,{'profile':profile, "proveedores_listado": proveedores_listado})
@login_required
def material_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        codigo= request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        categoria = request.POST.get('categoria')
        color = request.POST.get('color')
        precio = request.POST.get('precio')
        dimensiones = request.POST.get('dimensiones')
        cantidad = request.POST.get('cantidad')
        estado = request.POST.get('estado')

        if not codigo or not nombre or not categoria or not color or not precio or not dimensiones or not cantidad or not estado:
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('material_crear')

        material = Material(
            codigo=codigo,
            nombre=nombre,
            categoria=categoria,
            color=color,
            precio=precio,
            dimensiones=dimensiones,
            cantidad=cantidad,
            estado=estado
        )
        material.save()
        messages.add_message(request, messages.INFO, 'Material ingresado con éxito')
        return redirect('material_list')

    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')


@login_required
def material_ver(request, material_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tienes permisos')
        return redirect('check_group_main')
    material_data = Material.objects.get(pk=material_id)
    template_name = 'inventario/material_ver.html'
    return render(request, template_name, {'profile': profile, 'material_data': material_data})

@login_required
def material_list(request, page=None, search=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tiene permisos')
        return redirect('check_group_main')

    if page is None:
        page = request.GET.get('page')
    else:
        page = page

    if search is None:
        search = request.GET.get('search')
    else:
        search = search

    if request.method == 'POST':
        search = request.POST.get('search')
        page = None

    material_list = []
    if search is None or search == "None":
        material_count = Material.objects.filter().count()
        material_list_array = Material.objects.all().order_by('nombre')
        for material in material_list_array:
            material_list.append({
                'id' : material.id,
                'codigo': material.codigo,
                'nombre': material.nombre,
                'categoria': material.categoria,
                'color': material.color,
                'precio': material.precio,
                'dimensiones': material.dimensiones,
                'cantidad': material.cantidad,
                'estado': material.estado,
            })

    else:
        material_count = Material.objects.filter(nombre__icontains=search).count()
        material_list_array = Material.objects.filter(nombre__icontains=search).order_by('nombre')
        for material in material_list_array:
            material_list.append({
                'id' : material.id,
                'codigo': material.codigo,
                'nombre': material.nombre,
                'categoria': material.categoria,
                'color': material.color,
                'precio': material.precio,
                'dimensiones': material.dimensiones,
                'cantidad': material.cantidad,
                'estado': material.estado,
            })

    paginator = Paginator(material_list, 20)
    material_list_paginate = paginator.get_page(page)

    template_name = 'inventario/material_list.html'
    return render(request, template_name, {'template_name': template_name, 'material_list_paginate': material_list_paginate, 'paginator': paginator, 'page': page})

@login_required
def material_edit(request, material_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tiene permisos')
        return redirect('check_group_main')

    material = get_object_or_404(Material, id=material_id)

    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        categoria = request.POST.get('categoria')
        color = request.POST.get('color')
        precio = request.POST.get('precio')
        dimensiones = request.POST.get('dimensiones')
        cantidad = request.POST.get('cantidad')
        estado = request.POST.get('estado')

        material.codigo = codigo
        material.nombre = nombre
        material.categoria = categoria
        material.color = color
        material.precio = precio
        material.dimensiones = dimensiones
        material.cantidad = cantidad
        material.estado = estado
        material.save()

        return redirect('material_ver', material_id=material.id)
    else:
        template_name = 'inventario/material_edit.html'
        return render(request, template_name, {'material': material})

@login_required
def material_eliminar(request, material_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    material = get_object_or_404(Material, id=material_id)
    material.delete()
    messages.success(request, 'Material eliminado correctamente')
    return redirect('material_list')
@login_required
def generar_informe_material(request):
    filtro_nombre = request.GET.get('filtro_nombre', '')
    filtro_disponible = request.GET.get('filtro_disponible', '')
    filtro_utilizada = request.GET.get('filtro_utilizada', '')
    filtro_valor = request.GET.get('filtro_valor', '')

    materials = material.objects.all()

    if filtro_nombre:
        materials = materials.filter(nombre__icontains=filtro_nombre)

    if filtro_disponible:
        try:
            disponible = int(filtro_disponible)
            materials = materials.filter(cantidad_disponible=disponible)
        except ValueError:
            pass

    if filtro_utilizada:
        try:
            utilizada = int(filtro_utilizada)
            materials = materials.filter(cantidad_utilizada=utilizada)
        except ValueError:
            pass

    if filtro_valor:
        try:
            valor = float(filtro_valor)
            materials = materials.filter(valor_material=valor)
        except ValueError:
            pass

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="informe.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)

    data = [['Nombre', 'Descripción', 'Cantidad Disponible', 'Cantidad Utilizada', 'Valor del material', 'Proveedor']]

    for material in materials:
        data.append([
            material.nombre,
            material.descripcion,
            str(material.cantidad_disponible),
            str(material.cantidad_utilizada),
            str(material.valor_material),
            material.proveedor.nombre  # Reemplazar "proveedor.nombre" con el atributo adecuado del modelo Proveedor
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

######Clase Reserva ########
def reserva_crear(request):
    cancha_listado = Cancha.objects.all()
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'inventario/reserva_crear.html'
    return render(request, template_name, {"cancha_listado": cancha_listado})


@login_required
def reserva_eliminar(request, reserva_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    reserva = get_object_or_404(Reserva, id=reserva_id)
    reserva.delete()
    messages.success(request, 'reserva eliminada correctamente')
    return redirect('reserva_list')
@login_required
def reserva_ver(request, reserva_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')
    reserva_data = Reserva.objects.get(pk=reserva_id)
    template_name = 'inventario/reserva_ver.html'
    return render(request, template_name, {'profile': profile, 'reserva_data': reserva_data})
@login_required
def reserva_save(request):
    if request.method == 'POST':
        cancha_id = request.POST.get('Reserva')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        codigo= request.POST.get('codigo')
        reserva = Reserva(
            cancha_id=cancha_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            codigo=codigo
        )
        reserva.save()
        messages.add_message(request, messages.INFO, 'Reserva guardada exitosamente')
        return redirect('cancha_list')

    
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')
@login_required
def reserva_list(request, page=None, search=None):
    if page is None:
        page = request.GET.get('page')

    if search is None:
        search = request.GET.get('search')

    if request.method == 'POST':
        search = request.POST.get('search')
        page = None
    if request.method == 'POST':
        search = request.POST.get('search')
        page = None
    reserva_list = []
    if search is None or search == "None":
        reserva_count = Reserva.objects.all().count()
        reserva_list_array = Reserva.objects.all().order_by('cancha__nombre')
        for reserva in reserva_list_array:
            reserva_list.append({'id': reserva.id, 'cancha': reserva.cancha, 'fecha_inicio': reserva.fecha_inicio, 'fecha_fin': reserva.fecha_fin, 'codigo': reserva.codigo})

    else:
        reserva_count = Reserva.objects.filter(cancha__nombre__icontains=search).count()
        reserva_list_array = Reserva.objects.filter(cancha__nombre__icontains=search).order_by('cancha__nombre')
        for reserva in reserva_list_array:
            reserva_list.append({'id': reserva.id, 'cancha': reserva.cancha, 'fecha_inicio': reserva.fecha_inicio, 'fecha_fin': reserva.fecha_fin, 'codigo': reserva.codigo})

    paginator = Paginator(reserva_list, 20)
    reserva_list_paginate = paginator.get_page(page)

    template_name = 'inventario/reserva_list.html'
    return render(request, template_name, {'template_name': template_name, 'reserva_list_paginate': reserva_list_paginate, 'paginator': paginator, 'page': page})

@login_required
def reserva_edit(request, reserva_id):
    if request.method == 'POST':
        reserva = get_object_or_404(Reserva, id=reserva_id)
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        codigo= request.POST.get('codigo')
        reserva.fecha_inicio = fecha_inicio
        reserva.fecha_fin = fecha_fin
        reserva.codigo= codigo
        reserva.save()

        return redirect('reserva_ver', reserva_id=reserva.id)
    else:
        reserva_data = Reserva.objects.get(pk=reserva_id)
        template_name = 'inventario/reserva_ver.html'
        return render(request, template_name, {'reserva_data': reserva_data})
