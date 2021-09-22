from administrador.views import listarFactura
from django.db.models.indexes import Index
from django.shortcuts import redirect, render
from django.db import connection
from django.http import HttpResponse
from cliente.models import Huesped, OrdenDeCompra
from administrador.models import Habitacion
from .forms import huespedFechaForm,huespedForm,minutaForm, monedaForm
from typing import Text
from numpy import array, asarray
import numpy as np
import pandas as pd
import cx_Oracle
from datetime import datetime, date, timedelta
from django.utils import timezone
from cliente.models import Factura
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration
from django.template.loader import render_to_string
from account.models import User, Empleado,Cliente
from django.contrib import messages


#Iniciamos valores de variables.
huespedR = Huesped()
huespedes = []

#Pantalla de inicio del Cliente:
def portadacliente(request):
    try:    
            huespedes.clear()

            if(request.user.is_superuser):
                nombreCliente = request.user.username
            else:
                nombreCliente = request.user.cliente.nombre_empresa
            
            contexto = {
                'nombreCliente': nombreCliente
            }
            return render(request, 'portadacliente.html', contexto)    
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

def habitacion_planilla(request):
    try:
        valorMoneda = 1
        textoMoneda = '$'
        if 'idMoneda' in request.session:
            idMoneda = request.session['idMoneda']
            if idMoneda != None:
                valorMoneda = conseguirValorMoneda(int(idMoneda))
                textoMoneda = conseguirTextoMoneda(int(idMoneda))
        holaSoyUnArray = []
        if request.method == "POST":
            superDocumentoL = request.FILES['planilla-cliente']
            documentoLeido = pd.read_excel(superDocumentoL) 
            holaSoyUnArray = np.asarray(documentoLeido)
            print("ESTO SALIÓ" + str(holaSoyUnArray) )
            if(len(holaSoyUnArray) == 0):
                messages.warning(request, "ERROR: La planilla está mal formateada o vacía.")
                return redirect('habitacion-planilla')
                
            habiOcupada = False
            habiClonada = False
            for indice,huesped in enumerate(holaSoyUnArray):
                if habiClonada == True:
                    break
                habitacion = Habitacion.objects.get(numero_de_habitacion=huesped[4])
                if habitacion.disponibilidad_habitacion != 0:
                    habiOcupada = True
                    break
                for indicevali,huespedvali in enumerate(holaSoyUnArray):
                    if indicevali != indice:
                        if huesped[4] == huespedvali[4]:
                            habiClonada = True
                            break
            if habiOcupada == True or habiClonada == True:
                holaSoyUnArray = []
            precio = 0
            for huesped in holaSoyUnArray:
                habitacion = Habitacion.objects.get(numero_de_habitacion=huesped[4])
                # Indicarle al cliente que la fecha debe ser dia-mes-anho
                fechaInicio = datetime.strptime(huesped[2].strip(), '%m-%d-%Y').date()
                fechaFinal = datetime.strptime(huesped[3].strip(), '%m-%d-%Y').date()
                #AQUÍ VA A IR LA VALIDACIÓN DE FECHA.
                if(fechaInicio == fechaFinal):
                    messages.error(request, 'La fecha de inicio no puede ser identica a la fecha final (check-out): Problema en huésped que tiene el rut: ' + huesped[0])
                    listaHabitaciones.clear()

                    return redirect('habitacion-planilla')
                if(fechaInicio < date.today() ):
                    messages.error(request, 'La fecha de inicio no puede ser menor a la fecha de hoy: Problema en huésped que tiene el rut: ' + huesped[0])
                    listaHabitaciones.clear()

                    return redirect('habitacion-planilla')
                #VALIDACIÓN MÁXIMO TOTAL DE ESTADÍA.    
                # if(fechaFinal > date.today() + timedelta(weeks=52) ):
                #     messages.error(request, 'Para solicitar estadía mayor a un año por favor comunicarse con el hostal: Problema en huésped que tiene el rut: ' + huesped[0])
                #     return redirect('habitacion-planilla')
                if(fechaInicio > fechaFinal):
                    messages.error(request, 'La fecha de inicio no puede ser menor a la fecha de terminó: Problema en huésped que tiene el rut: ' + huesped[0])
                    listaHabitaciones.clear()

                    return redirect('habitacion-planilla')

                else:
                    listaHabitaciones = listarHabitacionDisp()
                    listaDescarteHabis  = habitacionesDescartadas(fechaInicio, fechaFinal)
                    descarte = False
                    numeroHabid = 0
                    print("descartando")
                    for habiDescarte in listaDescarteHabis:
                        descarte = False                       
                        if int(huesped[4]) == int(habiDescarte):
                            descarte =True
                            numeroHabid = str(habiDescarte)
                            break
                       

                    if(descarte):
                        messages.warning(request, "La habitación " + str(numeroHabid) + " no está disponible para el rango de fechas "+ str(fechaInicio) + " - " + str(fechaFinal))
                        listaHabitaciones.clear()
                        return redirect('habitacion-planilla')

                huesped[2] = fechaInicio
                huesped[3] = fechaFinal                
                print(type(huesped[2]))
                precio = habitacion.precio*(fechaFinal-fechaInicio).days
                huespedit = [huesped[0],huesped[1],huesped[4]
                ,huesped[2],huesped[3],precio]

                huespedes.append(huespedit)
            print(huespedes)

                    
        context = {'lista':listarHabitacionDisp(),
                    'listaHuesped': holaSoyUnArray,
                    'valorMoneda':valorMoneda,
                    'textoMoneda': textoMoneda}
        return render(request,'habitacion_planilla.html',context)

    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        messages.error(request, "Ha ocurrido un error al procesar la planilla, revisela o haga el ingreso manual.")
        return redirect('habitacion-planilla')

def lista_habitacion(request):
    try:
        listaHabitaciones = listarHabitacionDisp()
        #Descartamos habitaciones ocupadas. 
        print("LA LISTA DE HABIS:" + str(listaHabitaciones))
        if(huespedR != None):
            fechaInicio = huespedR.fecha_de_inicio
            fechaTermino = huespedR.fecha_de_termino

            listaDescarteHabis  = habitacionesDescartadas(fechaInicio, fechaTermino)
            descarte = False
            descartar = 0

            for habiDescarte in listaDescarteHabis:
                descarte = False
                print("descarte" + str(habiDescarte))
                for indiceHabi,habitacion in enumerate(listaHabitaciones):
                    print("habitacion:" + str(habitacion[1]))
                    if int(habitacion[1]) == int(habiDescarte):
                        descartar = indiceHabi
                        descarte =True
                        break
                if(descarte):
                    listaHabitaciones.pop(descartar)
                    print("descartando")
            


        valorMoneda = 1
        textoMoneda = '$'
        if 'idMoneda' in request.session:
            idMoneda = request.session['idMoneda']       
            if idMoneda != None:
                valorMoneda = conseguirValorMoneda(int(idMoneda))
                textoMoneda = conseguirTextoMoneda(int(idMoneda))
                print(valorMoneda)
        encontrador = False
        if len(huespedes) > 0:
            for huesped in huespedes:
                for habitacion in listaHabitaciones:
                    if huesped[2] == habitacion[1]:
                        habiDupli = listaHabitaciones.index(habitacion)
                        encontrador = True
                print(huesped[2],habitacion[1])
                if encontrador == True:
                    listaHabitaciones.pop(habiDupli)
                    encontrador = False

        
        context = {'lista': listaHabitaciones,
                'valorMoneda': valorMoneda,
                'textoMoneda': textoMoneda}

        return render(request, 'lista_habitacion.html', context)
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

def huesped(request,pk):
    try:
        habitacion = Habitacion.objects.get(numero_de_habitacion=pk)
        if request.method == 'POST':
            form = huespedForm(request.POST)
            if form.is_valid():
                huespedR.rut = form.cleaned_data['rut']
                huespedR.nombre = form.cleaned_data['nombre']
                # numero provisorio antes de ingresar a BD
                huespedR.orden_de_compra = 123
                huespedR.numero_de_habitacion = pk
                huespedR.precio = habitacion.precio*(huespedR.fecha_de_termino-huespedR.fecha_de_inicio).days
                print(huespedR.rut,huespedR.nombre,huespedR.numero_de_habitacion
                ,huespedR.fecha_de_inicio,huespedR.fecha_de_termino,huespedR.precio)

                huespedit = [huespedR.rut,huespedR.nombre,huespedR.numero_de_habitacion
                ,huespedR.fecha_de_inicio,huespedR.fecha_de_termino,huespedR.precio]

                huespedes.append(huespedit)
                cont = 0
                largo = len(huespedes)
                while cont<largo:
                    print(huespedes[cont])
                    cont+=1

                return redirect('cliente-habitacion')

        context = {'form': huespedForm(),
                'item': habitacion}
        return render(request, 'huesped_form.html', context)
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

def cliente(request):
    try:
        valorMoneda = 1
        textoMoneda = '$'
        if 'idMoneda' in request.session:
            idMoneda = request.session['idMoneda']
            if idMoneda != None:
                valorMoneda = conseguirValorMoneda(int(idMoneda))
                textoMoneda = conseguirTextoMoneda(int(idMoneda))


        if request.method == 'POST':
            form = huespedFechaForm(request.POST)
            if form.is_valid():
                huespedR.fecha_de_inicio = form.cleaned_data['fecha_de_inicio']
                huespedR.fecha_de_termino = form.cleaned_data['fecha_de_termino']
                if(huespedR.fecha_de_inicio > huespedR.fecha_de_termino):
                    messages.error(request, 'La fecha de inicio no puede ser menor a la fecha de terminó:' + str(huespedR.fecha_de_termino))

                    return redirect('cliente-habitacion')
                
                print(huespedR.fecha_de_inicio,huespedR.fecha_de_termino)
                print((huespedR.fecha_de_termino-huespedR.fecha_de_inicio).days)
                return redirect('lista-habitacion')
            if form.has_error:
                messages.error(request, 'La fecha de inicio no puede ser menor a la fecha de hoy.')

        context = {'form': huespedFechaForm(),
                'lista': huespedes,
                'valorMoneda': valorMoneda,
                'textoMoneda': textoMoneda}
        return render(request, 'cliente.html', context) 
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

def eliminar_huesped(request,pk):
    try:
        if request.method == 'POST':
            huespedes.pop(pk)
            return redirect('cliente-habitacion')
        context = {'item': pk}
        return render(request,'eliminar_huesped.html',context)
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

def descargar_excel(request):
    try:
        filename = "cliente/excel/planilla.xlsx"
        with open(filename, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/ms-excel')
            response['Content-Type'] = 'application/ms-excel'
            response['Content-Disposition'] = 'attachment; filename=planilla.xlsx'
            print(response)
            return response
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

def comedor(request):
    try:
            huespedes.clear()
            valorMoneda = 1
            textoMoneda = '$'
            if 'idMoneda' in request.session:
                idMoneda = request.session['idMoneda']
                if idMoneda != None:
                    valorMoneda = conseguirValorMoneda(int(idMoneda))
                    textoMoneda = conseguirTextoMoneda(int(idMoneda))
            listaPlatos = []
            minutaEncontrada = []
            if request.method =='POST':    
                formBuscarm=minutaForm(request.POST)
                if formBuscarm.is_valid():  
                    idcomedor = formBuscarm.cleaned_data['comedor']
                    minutaEncontrada=conseguirMinutaSemanal(idcomedor)
                    listaPlatos = []
                    platosLunes = ""
                    platosMartes = ""
                    platosMiercoles = ""
                    platosJueves = ""
                    platosViernes = ""
                    platosSabado = ""
                    platosDomingo = ""
                    valorPlato = 0            
                    if len(minutaEncontrada) > 0:
                        for indicePlato,plato in enumerate(minutaEncontrada):
                            if valorMoneda != 1:
                                    valorPlato = round(plato[4]/valorMoneda, 1)
                            else:
                                valorPlato = plato[4]//valorMoneda
                            if(plato[2] == 1):
                                if valorMoneda != 1:
                                    valorPlato = round(plato[4]/valorMoneda, 1)
                                else:
                                    valorPlato = plato[4]//valorMoneda                        
                                platosLunes = platosLunes + "\n   Nombre: " + str(plato[1]) + " \n Hora:" + str(plato[3])  + " \n Precio: "+ textoMoneda +  str(valorPlato) + " \n "
                            if(plato[2] == 2):
                                platosMartes = platosMartes + "\n   Nombre: " + str(plato[1]) + " \n Hora:" + str(plato[3])  + " \n Precio: "+ textoMoneda + str(valorPlato) + " \n "
                            if(plato[2] == 3):
                                platosMiercoles = platosMiercoles + "\n   Nombre: " + str(plato[1]) + " \n Hora:" + str(plato[3])  + " \n Precio: "+ textoMoneda + str(valorPlato) + " \n "
                            if(plato[2] == 4):
                                platosJueves = platosJueves + "\n   Nombre: " + str(plato[1]) + " \n Hora:" + str(plato[3])  + " \n Precio: "+ textoMoneda + str(valorPlato) + " \n "
                            if(plato[2] == 5):
                                platosViernes = platosViernes + "\n   Nombre: " + str(plato[1]) + " \n Hora:" + str(plato[3])  + " \n Precio: "+ textoMoneda +  str(valorPlato) + " \n "
                            if(plato[2] == 6):
                                platosSabado = platosSabado + "\n   Nombre: " + str(plato[1]) + " \n Hora:" + str(plato[3])  + " \n Precio: "+  textoMoneda + str(valorPlato) + " \n "
                            if(plato[2] == 7):
                                platosDomingo = platosDomingo + "\n   Nombre: " + str(plato[1]) + " \n Hora:" + str(plato[3])  + " \n Precio: "+ textoMoneda +  str(valorPlato) + " \n "
                    
                    listaPlatos.append(platosLunes)
                    listaPlatos.append(platosMartes)
                    listaPlatos.append(platosMiercoles)
                    listaPlatos.append(platosJueves)
                    listaPlatos.append(platosViernes)
                    listaPlatos.append(platosSabado)
                    listaPlatos.append(platosDomingo)
                    print(listaPlatos)

            data = {'form': minutaForm(),
                    'platos' : listaPlatos}

            return render(request, 'cliente_comedor.html',data)
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')    

def misCompras(request):
    try:
        huespedes.clear()
        if(request.user.is_superuser):
            rutCliente = '71369625-0'
        else:
            rutCliente = request.user.cliente.rut

        return render(request,'cliente_compras.html',context={'ordenCompra': listarOrdenPorCliente(rutCliente)})
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')
    
def compra_detalle(request,pk):
    try:
        

        numeroOrden = OrdenDeCompra.objects.get(pk=pk)
        factura = Factura.objects.filter(orden_de_compra_numero_oc=pk)
        huespedes = listarHuespedOC(int(pk))

        if(request.user.is_superuser):
            emisorFactura = Cliente.objects.filter(rut=numeroOrden.cliente_rut_empresa)
            if len(emisorFactura) > 0:
                nombreEmpresa = emisorFactura[0].nombre_empresa
                Rut = emisorFactura[0].rut
            else:
                nombreEmpresa = "ADMINISTRADOR " + request.user.username
                Rut = '71369625-0'
            direccion = 'Francisco Corral 297, Chonchi, Los Lagos'
            telefono = '9 9553 9757'
        else:
            nombreEmpresa = request.user.cliente.nombre_empresa
            Rut = request.user.cliente.rut
            direccion = request.user.cliente.direccion
            telefono = request.user.cliente.telefono



        print(huespedes)
        imprimiendo = False


        context = {'nombreEmpresa':nombreEmpresa,'Rut':Rut,
                    'direccion':direccion,'telefono':telefono,
                    'orden':numeroOrden,'factura':factura,'huesped':huespedes,
                    'imprimiendo': imprimiendo,
                    'codigoFactura':pk}

        return render(request,'compra-detalle.html',context)

    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

def listarOrdenPorCliente(rutCliente):
    try:
        listaOrden = []

        with connection.cursor() as cursorConsulta:
        #    print(cursorConsulta)
            cursorSalida = cursorConsulta.connection.cursor()
        #    print(cursorSalida)
            cursorConsulta.callproc('ORDENDECOMPRAPKG.listar_ordenescomprascliente', [rutCliente, cursorSalida])

        for orden in cursorSalida:
            listaOrden.append(orden)

        return listaOrden
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )

def listarHabitacionDisp():
    try:
        listaHabitaciones = []

        with connection.cursor() as cursorConsulta:
        #    print(cursorConsulta)
            cursorSalida = cursorConsulta.connection.cursor()
        #    print(cursorSalida)
            cursorConsulta.callproc('HABITACIONPKG.habitaciones_disponibles', [cursorSalida])

        for habitacion in cursorSalida:
            listaHabitaciones.append(habitacion)

        return listaHabitaciones
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )

def insertarHuesped(rut,nombre,orden_de_compra,numero,fecha_inicio,fecha_termino,precio,estadoH):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaHuespedBD = cursorConsulta.callfunc('HUESPEDPKG.insertar_huesped',Text,
            [rut,nombre,orden_de_compra,numero,fecha_inicio,fecha_termino,precio,estadoH])
        return respuestaHuespedBD
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )

def eliminarHuesped(id):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaServBD = cursorConsulta.callfunc('HUESPEDPKG.eliminar_huesped',Text,[id])
        return respuestaServBD
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )

def insertarOrdenDeCompra( fechaoc,valor_orden, rut_cliente_empresa):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaOrdenBD = cursorConsulta.callfunc('ORDENDECOMPRAPKG.insertar_ordendecompra',Text,
            [fechaoc,valor_orden,rut_cliente_empresa])

        return respuestaOrdenBD
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )

def eliminarOrdenDeCompra(numeroOrden):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaServBD = cursorConsulta.callfunc('ORDENDECOMPRAPKG.eliminar_ordendecompra',Text,[numeroOrden])
        return respuestaServBD
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )

def insertarFactura(fecha_emision, valor_bruto, valor_neto, precio_total, orden_de_compra):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaFacturaBD = cursorConsulta.callfunc('FACTURAPKG.insertar_factura',Text,
            [fecha_emision, valor_bruto, valor_neto,precio_total, orden_de_compra])

        return respuestaFacturaBD
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )

def conseguirNumeroOCA(rut):
    try:
        numerooca = 0
        with connection.cursor() as cursorConsulta:
            numerooca = cursorConsulta.var(cx_Oracle.NUMBER).var
            cursorConsulta.callproc('ORDENDECOMPRAPKG.leer_numeroocactual', [rut,numerooca])
        return numerooca
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
 
def liberarHabitacion(numeroOrden):
    try:
        mensaje = ''
        with connection.cursor() as cursorConsulta:
            mensaje = cursorConsulta.var(cx_Oracle.STRING).var
            cursorConsulta.callproc('ORDENDECOMPRAPKG.leer_numeroocactual', [numeroOrden,mensaje])
        return mensaje
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )


def conseguirMinutaSemanal(idcomedor):
    try:
        listaMinuta = []

        with connection.cursor() as cursorConsulta:
        #    print(cursorConsulta)
            cursorSalida = cursorConsulta.connection.cursor()
        #    print(cursorSalida)
            cursorConsulta.callproc('PLATOPKG.listar_minutasemanal', [idcomedor, cursorSalida])

        for minuta in cursorSalida:
            listaMinuta.append(minuta)

        return listaMinuta
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )


def confirmar_compra(request):
    try:
        tupleHuespedes = map(tuple,huespedes)
        if(len(huespedes) > len(set(tupleHuespedes))):
            indice = 0
            largoDupli = len(huespedes)
            while indice < largoDupli:
                indice += 1
                huespedes.pop(largoDupli-indice)
                
            print("Hay duplicados.")
            # Redirigir a pagina de errores
            return redirect('cliente-habitacion')
        valorMoneda = 1
        textoMoneda = '$'
        if 'idMoneda' in request.session:
            idMoneda = request.session['idMoneda']
            if idMoneda != None:
                valorMoneda = conseguirValorMoneda(int(idMoneda))
                textoMoneda = conseguirTextoMoneda(int(idMoneda))
        print(huespedes)
        precioTotal = 0
        for huesped in huespedes:
            precioTotal = precioTotal + (huesped[5])
        iva = 19
        precioFinalConIVA = precioTotal + round((precioTotal * iva)/100)
        ivaprecio = round((precioTotal * iva)/100)
        if request.method == 'POST':
            
  

            if(request.user.is_superuser):
                nombreEmpresa = "ADMINISTRADOR " + request.user.username
                Rut = '71369625-0'
                direccion = 'Francisco Corral 297, Chonchi, Los Lagos'
                telefono = '9 9553 9757'
                now = timezone.now()
                print(insertarOrdenDeCompra(now,precioTotal,'71369625-0'))
                errorInsertarHuesped = False
                huespedErroneo = 0
                numeroOrdenActual = conseguirNumeroOCA('71369625-0')
            else:            
                cliente = request.user.cliente
                now = timezone.now()
                print(insertarOrdenDeCompra(now,precioTotal,cliente.rut))
                errorInsertarHuesped = False
                huespedErroneo = 0
                numeroOrdenActual = conseguirNumeroOCA(cliente.rut)

            print("error de arriba ORDEN DE COMPRA")


            if numeroOrdenActual == None:
                print("Pagina error")
            print(numeroOrdenActual)
            for indiceHuesped,huesped in enumerate(huespedes):
                try:
                    #Estados Huesped: 0 inactivo, 1 activo, 2 tiene reserva
                    print(insertarHuesped(huesped[0],huesped[1],numeroOrdenActual,huesped[2],huesped[3],huesped[4],huesped[5],2))
                    print("error de arriba HUESPED")

                except: 
                    huespedErroneo = indiceHuesped
                    errorInsertarHuesped = False
                    break
            #En caso de que un huesped podido ingresarse. Se hace limpieza de datos y se arroja a una página de error.
            if(errorInsertarHuesped):
                for indiceBorrarH, huesped in enumerate(huespedes):
                    if(indiceBorrarH == huespedErroneo):
                        break
                    eliminar_huesped(huesped.id)
                    eliminarOrdenDeCompra(numeroOrdenActual)
                return "AQUI VA LA PÁGINA DE ERROR."
            tiempoActual = timezone.now()
            insertarFactura(tiempoActual,precioTotal,
            precioFinalConIVA,precioFinalConIVA,numeroOrdenActual)
            return redirect('factura')
            
        return render(request,'confirmar_compra.html',context={'lista':huespedes,'precioNeto':precioTotal,
                                                                'iva': ivaprecio, 'precioTotal': precioFinalConIVA, 'valorMoneda': valorMoneda,
                'textoMoneda': textoMoneda})
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

def factura(request):
    try:
        huespedes.clear()

        valorMoneda = 1
        textoMoneda = '$'
        if 'idMoneda' in request.session:
            idMoneda = request.session['idMoneda']
            if idMoneda != None:
                valorMoneda = conseguirValorMoneda(int(idMoneda))
                textoMoneda = conseguirTextoMoneda(int(idMoneda))

        if(request.user.is_superuser):

            nombreEmpresa = "ADMINISTRADOR" + request.user.username
            Rut = '71369625-0'
            direccion = 'Francisco Corral 297, Chonchi, Los Lagos'
            telefono = '9 9553 9757'
        else:            
            nombreEmpresa = request.user.cliente.nombre_empresa
            Rut = request.user.cliente.rut
            direccion = request.user.cliente.direccion
            telefono = request.user.cliente.telefono

        numeroActual = conseguirNumeroOCA(Rut)
        facturaActual = leerFactura(numeroActual)
        huespedActual = listarHuespedOC(numeroActual)

        imprimiendo = False

        

        context = {'nombreEmpresa':nombreEmpresa,'Rut':Rut,
                    'direccion':direccion,'telefono':telefono,
                    'factura':facturaActual,'huesped':huespedActual,'valorMoneda': valorMoneda,
                'textoMoneda': textoMoneda,
                'imprimiendo': imprimiendo}

        return render(request,'factura.html',context)  
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

def leerFactura(numeroOrden):
    try:
        with connection.cursor() as cursorConsulta:
            codigo_factura = cursorConsulta.var(cx_Oracle.NUMBER).var
            fecha_emision  = cursorConsulta.var(cx_Oracle.STRING).var
            valor_bruto    = cursorConsulta.var(cx_Oracle.NUMBER).var
            valor_neto     = cursorConsulta.var(cx_Oracle.NUMBER).var
            precio_total   = cursorConsulta.var(cx_Oracle.NUMBER).var
            cursorConsulta.callproc('FACTURAPKG.leer_facturaporoc', [numeroOrden,codigo_factura,fecha_emision, valor_bruto,
                                                                    valor_neto, precio_total])
        facturaEncontrada = [codigo_factura.getvalue(),fecha_emision.getvalue(), valor_bruto.getvalue(),valor_neto.getvalue(), precio_total.getvalue()]
        return facturaEncontrada
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')


def listarHuespedOC(numeroOC):
    try:
        listahuesped = []

        with connection.cursor() as cursorConsulta:
        #    print(cursorConsulta)
            cursorSalida = cursorConsulta.connection.cursor()
        #    print(cursorSalida)
            cursorConsulta.callproc('HUESPEDPKG.listar_huespedesNumOC', [numeroOC, cursorSalida])

        for minuta in cursorSalida:
            listahuesped.append(minuta)
            

        return listahuesped
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

#Sistema multimonetario
def actualizarMoneda(request):
    try:
        if request.method =='POST':        
            request.session['idMoneda'] = request.POST.get('sltTipoMoneda')
            print(request.session['idMoneda'])
            return redirect(request.META['HTTP_REFERER'])
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
       
def conseguirValorMoneda(idMoneda):
    try:
        with connection.cursor() as cursorConsulta:
            codigo_moneda = cursorConsulta.var(cx_Oracle.STRING).var
            valor_peso = cursorConsulta.var(cx_Oracle.NUMBER).var
            cursorConsulta.callproc('MONEDAPKG.leer_moneda', [idMoneda,codigo_moneda,valor_peso])
        #Si no devuelve nada retornará 1 peso.    
        if codigo_moneda.getvalue() == None: return 1 
        return valor_peso.getvalue()
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
  
def conseguirTextoMoneda(idMoneda):
    try:
        with connection.cursor() as cursorConsulta:
            codigo_moneda = cursorConsulta.var(cx_Oracle.STRING).var
            valor_peso = cursorConsulta.var(cx_Oracle.NUMBER).var
            cursorConsulta.callproc('MONEDAPKG.leer_moneda', [idMoneda,codigo_moneda,valor_peso])
        #Si no devuelve nada retornará 1 peso.    
        if codigo_moneda.getvalue() == None: return '$'
        return codigo_moneda.getvalue()
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )


def export_pdf_factura(request):
    try:
        valorMoneda = 1
        textoMoneda = '$'
        if 'idMoneda' in request.session:
            idMoneda = request.session['idMoneda']
            if idMoneda != None:
                valorMoneda = conseguirValorMoneda(int(idMoneda))
                textoMoneda = conseguirTextoMoneda(int(idMoneda))    

        if(request.user.is_superuser):
            nombreEmpresa = "ADMINISTRADOR " + request.user.username
            Rut = '71369625-0'
            direccion = 'Francisco Corral 297, Chonchi, Los Lagos'
            telefono = '9 9553 9757'
        else:
            nombreEmpresa = request.user.cliente.nombre_empresa
            Rut = request.user.cliente.rut
            direccion = request.user.cliente.direccion
            telefono = request.user.cliente.telefono          

        numeroActual = conseguirNumeroOCA(Rut)
        facturaActual = leerFactura(numeroActual)
        huespedActual = listarHuespedOC(numeroActual)


        imprimiendo = True

        context = {'nombreEmpresa':nombreEmpresa,'Rut':Rut,
                    'direccion':direccion,'telefono':telefono,
                    'factura':facturaActual,'huesped':huespedActual,'valorMoneda': valorMoneda,
                'textoMoneda': textoMoneda,
                'imprimiendo': imprimiendo}


        html = render_to_string("factura.html", context)

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "inline; Factura.pdf"

        font_config = FontConfiguration()
        HTML(string=html).write_pdf(response, font_config=font_config)

        return response
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')

def export_pdf_mis_compras(request,pk):
    try:
        valorMoneda = 1
        textoMoneda = '$'
        if 'idMoneda' in request.session:
            idMoneda = request.session['idMoneda']
            if idMoneda != None:
                valorMoneda = conseguirValorMoneda(int(idMoneda))
                textoMoneda = conseguirTextoMoneda(int(idMoneda))  


        numeroOrden = OrdenDeCompra.objects.get(pk=pk)
        factura = Factura.objects.filter(orden_de_compra_numero_oc=pk)
        huespedes = listarHuespedOC(int(pk))
        pk = pk
          
        if(request.user.is_superuser):
            emisorFactura = Cliente.objects.filter(rut=numeroOrden.cliente_rut_empresa)
            if len(emisorFactura) > 0:
                nombreEmpresa = emisorFactura[0].nombre_empresa
                Rut = emisorFactura[0].rut
            else:
                nombreEmpresa = "ADMINISTRADOR " + request.user.username
                Rut = '71369625-0'
            direccion = 'Francisco Corral 297, Chonchi, Los Lagos'
            telefono = '9 9553 9757'
        else:
            nombreEmpresa = request.user.cliente.nombre_empresa
            Rut = request.user.cliente.rut
            direccion = request.user.cliente.direccion
            telefono = request.user.cliente.telefono  


  

        imprimiendo = True

        context = {'nombreEmpresa':nombreEmpresa,'Rut':Rut,
                    'direccion':direccion,'telefono':telefono,
                    'orden':numeroOrden,'factura':factura,'huesped':huespedes,'pk':pk,'valorMoneda': valorMoneda,
                'textoMoneda': textoMoneda,
                'imprimiendo': imprimiendo,
                'codigoFactura':pk}


        html = render_to_string("compra-detalle.html", context)

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "inline; Factura.pdf"

        font_config = FontConfiguration()
        HTML(string=html).write_pdf(response, font_config=font_config)

        return response

    except Exception as infoErrorm:
                print("ERROR " + str(infoErrorm) )
                return redirect('paginaerror')


#Algoritmo para validarFechas 
def habitacionesDescartadas(fechaInicio, fechaTermino):
    habisDescartadas = []
    with connection.cursor() as cursor:
        #Primero se válida que la fecha de inicio no esté ocupada. 
        cursor.execute("SELECT numero_de_habitacion FROM cliente_huesped WHERE (%s BETWEEN fecha_de_inicio and fecha_de_termino);",[fechaInicio])
        habisOcupadasfi = cursor.fetchall()
        for habitacion in habisOcupadasfi:
            habisDescartadas.append(int(habitacion[0]))
        cursor.execute("SELECT numero_de_habitacion FROM cliente_huesped WHERE ( fecha_de_inicio = %s);",[fechaInicio])
        habisOcupadasfimd = cursor.fetchall()
        for habitacion in habisOcupadasfimd:
            habisDescartadas.append(int(habitacion[0]))
        cursor.execute("SELECT numero_de_habitacion FROM cliente_huesped WHERE ( fecha_de_termino = %s);",[fechaInicio])
        habisOcupadasfimft = cursor.fetchall()
        for habitacion in habisOcupadasfimft:
            habisDescartadas.append(int(habitacion[0]))
        #Segundo se válida que la fecha de termino no esté ocupada. 
        cursor.execute("SELECT numero_de_habitacion FROM cliente_huesped WHERE (%s BETWEEN fecha_de_inicio and fecha_de_termino);",[fechaTermino])
        habisOcupadasft = cursor.fetchall()
        for habitacion in habisOcupadasft:
            habisDescartadas.append(int(habitacion[0])) 
        cursor.execute("SELECT numero_de_habitacion FROM cliente_huesped WHERE (fecha_de_termino = %s);",[fechaTermino])
        habisOcupadasftmd = cursor.fetchall()
        for habitacion in habisOcupadasftmd:
            habisDescartadas.append(int(habitacion[0])) 
        cursor.execute("SELECT numero_de_habitacion FROM cliente_huesped WHERE (fecha_de_inicio = %s);",[fechaTermino])
        habisOcupadasftmfi = cursor.fetchall()
        for habitacion in habisOcupadasftmfi:
            habisDescartadas.append(int(habitacion[0])) 

        #Finalmente validamos las propias fechas del hostal.
        cursor.execute("SELECT numero_de_habitacion FROM cliente_huesped WHERE (fecha_de_inicio BETWEEN %s and %s);",[fechaInicio, fechaTermino])
        habisOcupadasnfi = cursor.fetchall()
        for habitacion in habisOcupadasnfi:
            habisDescartadas.append(int(habitacion[0])) 
        cursor.execute("SELECT numero_de_habitacion FROM cliente_huesped WHERE (fecha_de_termino BETWEEN %s and %s);",[fechaInicio, fechaTermino])
        habisOcupadasnft = cursor.fetchall()
        for habitacion in habisOcupadasnft:
            habisDescartadas.append(int(habitacion[0])) 
    return habisDescartadas

#Ayuda al cliente
def ayudacliente(request):
    try:
        return render(request, 'ayudacliente.html')
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')

#Información de habitaciones
def infohabitaciones(request):
    try:
        huespedes.clear()

        return render(request, 'infohabitaciones.html')
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')

#Información de comedores
def infocomedores(request):
    try:
        huespedes.clear()

        return render(request, 'infocomedores.html')
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')