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
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

@login_required
def proveedoreses_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedoreses/proveedoreses_main.html'
    return render(request,template_name,{'profile':profile})

@login_required
def gestion_proveedoreses(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedoreses/gestion_proveedoreses.html'
    return render(request,template_name,{'profile':profile})
@login_required
def orden_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedoreses/orden_main.html'
    return render(request,template_name,{'profile':profile})
@login_required
def gestion_de_orden(request):
    arriendosListados= Arriendo.objects.all()
    proveedoreses_listado= proveedores.objects.all()
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedoreses/gestion_de_orden.html'
    return render(request,template_name,{"arriendos": arriendosListados, "proveedoreses_listado": proveedoreses_listado})

    
@login_required
def gestion_ver(request):
    arriendosListados= Arriendo.objects.all()
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedoreses/gestion_ver.html'
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
        proveedores_nombre=proveedores.objects.get (id=nombre)
        
        arriendo_save = Arriendo(
            nombre = proveedores_nombre,
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
    template_name = 'proveedoreses/orden_add.html'
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
        orden_save = proveedores(
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

    template_name = 'proveedoreses/gestion_ver.html'
    return render(request, template_name, {
        'template_name': template_name,
        'arriendos': arriendosListados,
        'gestion_ver_paginate': gestion_ver_paginate,
        'paginator': paginator,
        'page': page,
    })



#eliminar
@login_required
def orden_ver(request,proveedores_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    proveedores_data = proveedores.objects.get(pk=proveedores_id)
    template_name = 'proveedoreses/orden_ver.html'
    return render(request,template_name,{'profile':profile,'proveedores_data':proveedores_data})

@login_required
def eliminar_orden(request, proveedores_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    proveedores = get_object_or_404(proveedores, id=proveedores_id)
    proveedores.delete()
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
        h_count = proveedores.objects.count()
        h_list_array = proveedores.objects.order_by('nivel')
        for h in h_list_array:
            h_list.append({'id': h.id, 'nombre': h.nombre, 'nivel': h.nivel, 'hora': h.hora})
    else:
        h_count = proveedores.objects.filter(nombre__icontains=search).count()
        h_list_array = proveedores.objects.filter(nombre__icontains=search).order_by('nombre')
        for h in h_list_array:
            h_list.append({'id': h.id, 'nombre': h.nombre, 'nivel': h.nivel, 'hora': h.hora})

    paginator = Paginator(h_list, 20)
    h_list_paginate = paginator.get_page(page)
    template_name = 'proveedoreses/orden_list.html'
    return render(request, template_name, {'template_name': template_name, 'h_list_paginate': h_list_paginate, 'paginator': paginator, 'page': page})
@login_required
def orden_proveedores_edit(request, proveedores_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    proveedores = get_object_or_404(proveedores, id=proveedores_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        nivel = request.POST.get('nivel')
        hora = request.POST.get('hora')

        proveedores.nombre = nombre
        proveedores.nivel = nivel
        proveedores.hora = hora
        proveedores.save()

        return redirect('orden_ver', proveedores_id=proveedores.id)
    else:
        proveedores_data = proveedores.objects.get(pk=proveedores_id)
        template_name= 'proveedoreses/proveedoreses_ver.html'
        return render(request, template_name, {'proveedores_data': proveedores_data})
##################################################################################
# proveedores crear #

@login_required
def proveedoreses_crear(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedoreses/proveedoreses_crear.html'
    return render(request,template_name,{'profile':profile})

# proveedores guardar #

@login_required
def proveedores_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')    
        rubro= request.POST.get('rubro') 
        email = request.POST.get('email') 
        telefono = request.POST.get('telefono') 
        rut = request.POST.get('rut') 

        if nombre == '' or rubro == '' or email == '' or telefono == '' or rut == '':
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('proveedores_crear')

        proveedores = proveedores(
            nombre=nombre,
            rubro=rubro,  
            email=email,
            telefono=telefono,
            rut=rut 
        )
        proveedores.save()
        messages.add_message(request, messages.INFO, 'proveedores ingresado con éxito')
        return redirect('gestion_proveedoreses')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')


# proveedores listar #


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
        h_count = proveedores.objects.filter().count()
        h_list_array = proveedores.objects.filter().order_by('nombre')
        for h in h_list_array:
            h_list.append({'id': h.id, 'nombre': h.nombre})
    else:
        h_count = proveedores.objects.filter(nombre__icontains=search).count()
        h_list_array = proveedores.objects.filter(nombre__icontains=search).order_by('nombre')
        for h in h_list_array:
            h_list.append({'id': h.id, 'nombre': h.nombre})

    paginator = Paginator(h_list, 20)
    h_list_paginate = paginator.get_page(page)

    template_name = 'proveedoreses/proveedoreses_list.html'
    return render(request, template_name, {'template_name': template_name, 'h_list_paginate': h_list_paginate,
                                           'paginator': paginator, 'page': page})


# proveedores ver #

@login_required
def proveedores_ver(request, proveedores_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tienes permisos')
        return redirect('check_group_main')
    proveedores_data = proveedores.objects.get(pk=proveedores_id)
    template_name = 'proveedoreses/proveedoreses_ver.html'
    return render (request, template_name, {'profile': profile, 'material_data': proveedores_data})

# proveedores editar #

@login_required
def proveedores_edit(request, proveedores_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    proveedores = get_object_or_404(proveedores, id=proveedores_id)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        rubro = request.POST.get('rubro')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        rut = request.POST.get('rut')

        proveedores.nombre = nombre
        proveedores.rubro = rubro 
        proveedores.email = email
        proveedores.telefono = telefono
        proveedores.rut = rut
        proveedores.save()

        return redirect('proveedoreses_ver', proveedores_id=proveedores.id)
    else:
        proveedores_data = proveedores.objects.get(pk=proveedores_id)
        template_name= 'proveedoreses/proveedores_edit.html'
        return render(request, template_name, {'proveedores_data': proveedores_data})



# proveedores eliminar #

@login_required
def proveedores_eliminar(request, proveedores_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    proveedores = get_object_or_404(proveedores, id=proveedores_id)
    proveedores.delete()
    messages.success(request, 'proveedores eliminado correctamente')
    return redirect(reverse('proveedoreses_list'))
