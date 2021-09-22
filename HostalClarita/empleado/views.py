from account.models import Empleado, Proveedor, User
from django.db.models.indexes import Index
from django.shortcuts import redirect, render
from django.db import connection
from django.http import HttpResponse
from typing import Text
from numpy import array, asarray
import numpy as np
import pandas as pd
import cx_Oracle
from datetime import datetime, date
from django.utils import timezone
from .forms import proveedoresForm
from django.contrib import messages



#Aquí es en dónde puede solicitar productos y crear la orden de pedido.
carritoDeCompras = []


#Portada empleado
def empleado(request):
    try:
        carritoDeCompras.clear()
        request.session['proveedorActual'] = None
        if(request.user.is_superuser):
            nombreEmpleado = request.user.username
        else:
            nombreEmpleado = request.user.empleado.nombre_completo_empleado
        contexto = {
            'nombreEmpleado': nombreEmpleado
        }
        return render(request, 'empleado.html', contexto)
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')


def crearpedido(request):
    try:
        listaDeProductos = []
        if 'proveedorActual' in request.session:
            idProvActual = request.session['proveedorActual']
            if idProvActual != None:
                listaDeProductos = listarProductosProv(int(idProvActual))

        if request.method == 'POST':
            formProveedores = proveedoresForm(request.POST)
            if formProveedores.is_valid():
                proveedorSld = formProveedores.cleaned_data['proveedores']
                listaDeProductos = listarProductosProv(int(proveedorSld.user.id))
                request.session['proveedorActual'] = proveedorSld.user.id
                print(listaDeProductos)  
                carritoDeCompras.clear() 
            if 'btnAgregarAlCarro' in request.POST:
                productoNuevo = True
                if len(carritoDeCompras) > 0:
                    indiceActualProdu = int(request.POST.get('btnAgregarAlCarro'))
                    for indiceListaP,productoEncontrado in enumerate(listaDeProductos):
                        if indiceListaP == int(request.POST.get('btnAgregarAlCarro')):
                            for productoCarrito in carritoDeCompras:
                                if int(productoEncontrado[0]) == int(productoCarrito[0]):
                                    productoCarrito[6] = int(productoEncontrado[6]) * int(request.POST.get('cantidadProductos'))
                                    productoCarrito[7] = int(request.POST.get('cantidadProductos'))
                                    productoNuevo = False  
                                           
                if(productoNuevo):
                    producto = []
                    for indiceListaP,productoEncontrado in enumerate(listaDeProductos):
                        if indiceListaP == int(request.POST.get('btnAgregarAlCarro')):
                            producto.append(int(productoEncontrado[0])) #id
                            producto.append(int(productoEncontrado[1])) #codigo
                            producto.append(productoEncontrado[2]) #nombre
                            producto.append(productoEncontrado[3]) 
                            producto.append(productoEncontrado[4])
                            producto.append(productoEncontrado[5])
                            producto.append(int(productoEncontrado[6]) * int(request.POST.get('cantidadProductos')))
                            producto.append(int(request.POST.get('cantidadProductos'))) #Cantidad
                            break                
                    carritoDeCompras.append(producto)
                    print(carritoDeCompras)
                print(request.POST.get('btnAgregarAlCarro'))
                print(request.POST.get('cantidadProductos'))

            if 'btnElimDelCarro' in request.POST:
                indiceProdQuitado = int(request.POST.get('btnElimDelCarro'))
                carritoDeCompras.pop(indiceProdQuitado)   
        contexto = {'formProveedores':proveedoresForm(),
                    'listaDeProductos': listaDeProductos,
                    'carritoDeCompras': carritoDeCompras}
        return render(request, 'crear_pedido.html',contexto)
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

#View para ver el nuevo pedido
def mostrarpedidonuevo(request):
    try:     
        if(len(carritoDeCompras) == 0):
            return redirect('crearpedido')
        if request.session['proveedorActual'] == None:
            return redirect('crearpedido')


        dataPedido = []
        tiempoActual = timezone.now()
        valorTotal = 0
        idProvActual = request.session['proveedorActual']
        for productoCarrito in carritoDeCompras:
            valorTotal = valorTotal + productoCarrito[6]
        proveedorActual = User.objects.filter(id=int(idProvActual)).first()
        if(request.user.is_superuser):
            print(insertarOrdenDePedido(tiempoActual, 0, valorTotal, None, '71369625-0', proveedorActual.proveedor.rut))
            opActual = conseguirNumeroOPA('71369625-0')
        else:
            print(insertarOrdenDePedido(tiempoActual, 0, valorTotal, None, request.user.empleado.rut, proveedorActual.proveedor.rut))
            opActual = conseguirNumeroOPA(request.user.empleado.rut)

        for productoCarrito in carritoDeCompras:
            insertarDetalleDePedido(int(productoCarrito[7]), int(productoCarrito[6]),int(productoCarrito[1]), int(opActual))
            dataPedido.append(productoCarrito)
    
        print(dataPedido)
        if(request.user.is_superuser):
            datosProveedor = proveedorActual.proveedor.nombre_proveedor + ' Rut:' + proveedorActual.proveedor.rut 
            datosSolicitante = 'Administrador ' + request.user.username + ' Rut:' +   '71369625-0'     
        else:        
            datosProveedor = proveedorActual.proveedor.nombre_proveedor + ' Rut:' + proveedorActual.proveedor.rut 
            datosSolicitante = request.user.empleado.nombre_completo_empleado + ' Rut:' +   request.user.empleado.rut 
  
        contexto = {'dataPedido': dataPedido,
                    'valorTotal': valorTotal,
                    'idop': opActual,
                    'datosProveedor': datosProveedor,
                    'datosSolicitante':  datosSolicitante}


        carritoDeCompras.clear()
        request.session['proveedorActual'] = None
        return render(request, 'mostrar_pedidonuevo.html',contexto)
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')


#View para administrar los pedidos
def administrarpedido(request):
    try:     
        carritoDeCompras.clear()
        request.session['proveedorActual'] = None
        # ESTADOS DE ORDEN DE PEDIDO
        # 0: creados.
        # 1: pendiente.
        # 2: entregada:
        # 3: rechazada.
        # 4: cancelada.
        # 5: aceptada.

        #ARRAY GENERADO DE ORDEN DE PEDIDO
        # 0(idOp)    
        # 1(fechacodp.getvalue())    
        # 2(estadoodp.getvalue()) 
        # 3(precioTotal.getvalue())    
        # 4(fecharodp.getvalue())    
        # 5 rutEmpleado.getvalue())    
        # 6 rutProveedor.getvalue())    
        if 'btnEnviarPedido' in request.POST:
            idEnviarOP = int(request.POST.get('btnEnviarPedido'))
            opPreparada = leerOrdenPedido(idEnviarOP)
            tiempoActual = timezone.now()

            print(actualizarOrdenPedido(opPreparada[0],tiempoActual,1,opPreparada[3],tiempoActual,opPreparada[5],opPreparada[6]))
            messages.success(request, "La orden de pedido ha sido enviada al proveedor con éxito.")  


        if 'btnEliminarPedido' in request.POST:
            opNoDeseado = int(request.POST.get('btnEliminarPedido'))
            print(eliminarOP(opNoDeseado))
            messages.info(request, "La orden de pedido ha sido eliminada con éxito.")  

   
        if 'btnEliminarPedidoAP' in request.POST:
            opNoDeseado = int(request.POST.get('btnEliminarPedidoAP'))
            print(eliminarOP(opNoDeseado))
            messages.info(request, "La orden de pedido ha sido eliminada con éxito.")  
            return redirect('admin-pedidos')


        if 'btnRechazarOP' in request.POST:
            idOpRechazada = int(request.POST.get('btnRechazarOP'))
            opRechazada = leerOrdenPedido(idOpRechazada)
            print(actualizarOrdenPedido(opRechazada[0],opRechazada[1],3,opRechazada[3],opRechazada[4],opRechazada[5],opRechazada[6]))   
            #ACTUALIZAR STOCK
            listaDetallesOP = listarDetalleOP(idOpRechazada)
            for detalleConsulta in listaDetallesOP:
                # detalleEncontrado.append(idDetalle)    
                # detalleEncontrado.append(cantidadProdu.getvalue())    
                # detalleEncontrado.append(precioPedi.getvalue()) 
                # detalleEncontrado.append(codigoProducto.getvalue())    
                # detalleEncontrado.append(idOdp.getvalue())
                productoEncontrado =  leerProductoPorCodigo(detalleConsulta[3])
                actualizarStockProducto(detalleConsulta[3],(productoEncontrado[4] + detalleConsulta[1]))       
            messages.info(request, "Pedido rechazado con éxito.")  


        if 'btnAceptarProductos' in request.POST:
            idOpAceptada = int(request.POST.get('btnAceptarProductos'))
            opAceptada = leerOrdenPedido(idOpAceptada)
            print(actualizarOrdenPedido(opAceptada[0],opAceptada[1],5,opAceptada[3],opAceptada[4],opAceptada[5],opAceptada[6])) 
            messages.success(request, "El pedido ha sido aceptado con éxito.")  

        pedidosPorRecepcionar =  listarOpPorEstado(2)
        pedidosPendientes =  listarOpPorEstado(1)
        pedidosCreados = listarOpPorEstado(0)
        contexto = {'listaPedidosCreados' : pedidosCreados,
                    'listaPedidosPendientes': pedidosPendientes,
                    'listaPedidosPorRecibir':pedidosPorRecepcionar}
        return render(request, 'administrar_pedido.html',contexto)
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

#View para modificar los pedidos
def modificarpedido(request):
    try:     
        listaProductosOP = []
        listaDetallesOP = []
        ordenEncontrada = []
        if(request.user.is_superuser):
            rutEmpleadoActual = request.user.username
        else:
            rutEmpleadoActual = request.user.empleado.rut
        datosSolicitante = ''
        datosProveedor = ''

        if 'btnModificarPedido' in request.POST:
            request.session['modiOrdenActual'] = int(request.POST.get('btnModificarPedido'))

        if 'modiOrdenActual' in request.session:
            opParaModificar = request.session['modiOrdenActual']
            if opParaModificar != None:
                ordenEncontrada = leerOrdenPedido(opParaModificar)

        if 'btnEliminarProdu' in request.POST:
                idDetalleEli = int(request.POST.get('btnEliminarProdu'))
                eliminarDetalleOP(idDetalleEli)
                listaDetallesOP = listarDetalleOP(opParaModificar)
                totalParaPagar = 0
                for detalleConsulta in listaDetallesOP:
                   totalParaPagar = totalParaPagar + detalleConsulta[2]
                if(len(listaDetallesOP) != 0):
                    actualizarOrdenPedido(ordenEncontrada[0],ordenEncontrada[1],ordenEncontrada[2],totalParaPagar,ordenEncontrada[4],rutEmpleadoActual,ordenEncontrada[6])      
                else:
                    eliminarOP(int(ordenEncontrada[0]))
                    return redirect('administrarpedido')
                messages.info(request, "El producto ha sido quitado de la orden de pedido con éxito.")  

        if 'btnActualizarProdu' in request.POST:
                idDetalleModi = int(request.POST.get('btnActualizarProdu'))
                nuevaCantidad = int(request.POST.get('nuevaCantidadProd'))
                detalleEncontrado = leerDetalleOP(idDetalleModi)
                        # detalleEncontrado.append(idDetalle)    
                        # detalleEncontrado.append(cantidadProdu.getvalue())    
                        # detalleEncontrado.append(precioPedi.getvalue()) 
                        # detalleEncontrado.append(codigoProducto.getvalue())    
                        # detalleEncontrado.append(idOdp.getvalue())
                productoConsulta = leerProductoPorCodigo(detalleEncontrado[3])   
                actualizarDetalleOP(detalleEncontrado[0],nuevaCantidad,(round(int(productoConsulta[7]) * nuevaCantidad)),detalleEncontrado[3],detalleEncontrado[4])
                listaDetallesOP = listarDetalleOP(opParaModificar)
                totalParaPagar = 0
                for detalleConsulta in listaDetallesOP:
                   totalParaPagar = totalParaPagar + detalleConsulta[2]
                actualizarOrdenPedido(ordenEncontrada[0],ordenEncontrada[1],ordenEncontrada[2],totalParaPagar,ordenEncontrada[4],rutEmpleadoActual,ordenEncontrada[6])      
                ordenEncontrada = leerOrdenPedido(opParaModificar)
                messages.success(request, "La orden de pedido ha sido actualizada con éxito.")  

        listaDetallesOP = listarDetalleOP(opParaModificar)
        for detalle in listaDetallesOP:
            productoEncontrado = leerProductoPorCodigo(detalle[3])
            #CANTIDAD
            productoEncontrado.append(detalle[1]) 
            #TOTAL PAGADO
            productoEncontrado.append(detalle[2]) 
            #ID detalle orden pedido
            productoEncontrado.append(detalle[0])
            listaProductosOP.append(productoEncontrado)
            print(listaProductosOP)
            
            #ARRAY GENERADO DE PRODUCTOS
            # 1 nombreProducto 
            # 2 marcaProducto
            # 3 descripcionProdu 
            # 4 stockProdu
            # 5 stockCriticoProdu 
            # 6 fechaVenciProdu 
            # 7 precioProdu 
            # 8 idProveedor
            # 9 familiaProducto
            # 10 CANTIDAD PEDIDO
            # 11 TOTAL PAGADO
            # 12 idDetalle
           

           #ARRAY GENERADO DE ORDEN DE PEDIDO
        # 0(idOp)    
        # 1(fechacodp.getvalue())    
        # 2(estadoodp.getvalue()) 
        # 3(precioTotal.getvalue())    
        # 4(fecharodp.getvalue())    
        # 5 rutEmpleado.getvalue())    
        # 6 rutProveedor.getvalue())    

        numeroOrden = ordenEncontrada[0]
        fechaCreacion = ordenEncontrada[1]
        precioTotal = ordenEncontrada[3]

        proveedorOP = Proveedor.objects.filter(rut=str(ordenEncontrada[6])).first()
        solicitanteOP = Empleado.objects.filter(rut=str(ordenEncontrada[5])).first()
        datosProveedor = proveedorOP.nombre_proveedor + ' Rut:' + proveedorOP.rut 

        if solicitanteOP != None:
            datosSolicitante = solicitanteOP.nombre_completo_empleado + ' Rut:' +   solicitanteOP.rut 
        else:            
            datosSolicitante = 'UN ADMINISTRADOR' + ' Rut:' +   '71369625-0'
            if proveedorOP != None: 
                datosProveedor = proveedorOP.nombre_proveedor + ' Rut:' + proveedorOP.rut 
            else:
                datosProveedor = 'UN ADMINISTRADOR' + ' Rut:' +  '71369625-0'



        contexto = {'listaProductosOP': listaProductosOP,
        'numeroOrden': numeroOrden,
        'fechaCreacion': fechaCreacion,
        'precioTotal': precioTotal,
        'datosSolicitante':datosSolicitante,
        'datosProveedor': datosProveedor}

        return render(request, 'modificar_pedido.html', contexto)
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')





#View para ver los pedidos
def mostrarpedido(request):
    try:     
        listaProductosOP = []
        listaDetallesOP = []
        ordenEncontrada = []
        numeroOrden = 0
        fechaCreacion = 0
        precioTotal = 0
        datosSolicitante = ''
        datosProveedor = ''

        if 'btnVerDetallePedido' in request.POST:
            idLeerOP = int(request.POST.get('btnVerDetallePedido'))
            ordenPedidoConsulta = leerOrdenPedido(idLeerOP)
            numeroOrden = ordenPedidoConsulta[0]
            fechaCreacion = ordenPedidoConsulta[1]
            precioTotal = ordenPedidoConsulta[3]
            listaDetallesOP = listarDetalleOP(idLeerOP)
            for detalle in listaDetallesOP:
                productoEncontrado = leerProductoPorCodigo(detalle[3])
                #CANTIDAD
                productoEncontrado.append(detalle[1]) 
                #TOTAL PAGADO
                productoEncontrado.append(detalle[2]) 
                #ID detalle orden pedido
                productoEncontrado.append(detalle[0])
                listaProductosOP.append(productoEncontrado)      
                      
            proveedorOP = Proveedor.objects.filter(rut=str(ordenPedidoConsulta[6])).first()
            solicitanteOP = Empleado.objects.filter(rut=str(ordenPedidoConsulta[5])).first()
            datosProveedor = proveedorOP.nombre_proveedor + ' Rut:' + proveedorOP.rut 

            if solicitanteOP != None:
                datosSolicitante = solicitanteOP.nombre_completo_empleado + ' Rut:' +   solicitanteOP.rut 
            else:            
                datosSolicitante = 'UN ADMINISTRADOR' + ' Rut:' +   '71369625-0'
                if proveedorOP != None: 
                    datosProveedor = proveedorOP.nombre_proveedor + ' Rut:' + proveedorOP.rut 
                else:
                    datosProveedor = 'UN ADMINISTRADOR' + ' Rut:' +  '71369625-0'


        contexto = {'listaProductosOP': listaProductosOP,
        'numeroOrden': numeroOrden,
        'fechaCreacion': fechaCreacion,
        'precioTotal': precioTotal,
        'datosSolicitante':datosSolicitante,
        'datosProveedor': datosProveedor}


        return render(request, 'mostrar_pedido.html',contexto)
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')






#Historial de Pedidos
def historialpedidos(request):
    try:
        carritoDeCompras.clear()
        request.session['proveedorActual'] = None
        #PEDIDOS
        # 0: creados.
        # 1: pendiente.
        # 2: entregada:
        # 3: rechazada.
        # 4: cancelada.
        # 5: aceptada.
        

        lpedidosAceptados = listarOpPorEstado(5)
        lpedidosRechazados  = listarOpPorEstado(3)
        lpedidosEntregados =  listarOpPorEstado(2)
        lpedidosCancelados = listarOpPorEstado(4)
        contexto = {'lpedidosAceptados':lpedidosAceptados,
                'lpedidosRechazados':lpedidosRechazados,
                'lpedidosEntregados':lpedidosEntregados,
                'lpedidosCancelados':lpedidosCancelados}
        return render(request, 'historial_pedidos.html',contexto)

    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')







#Procedimientos almacenados de productos y proveedor
#Procedimiento almacenado para listar productos por proveedor.
#Actualizar stock de producto
def actualizarStockProducto(codigoProducto,stock):  
    try:  
        with connection.cursor() as cursorConsulta:
            respuestaServBD = cursorConsulta.callfunc('PRODUCTOPKG.actualizar_stockproducto', Text, [codigoProducto,stock])    
        return respuestaServBD
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )

def listarProductosProv(idProveedor):
    try:
        listaProductos = []

        with connection.cursor() as cursorConsulta:
        #    print(cursorConsulta)
            cursorSalida = cursorConsulta.connection.cursor()
        #    print(cursorSalida)
            cursorConsulta.callproc('PRODUCTOPKG.listar_productosprov', [idProveedor, cursorSalida])

        for producto in cursorSalida:
            listaProductos.append(producto)

        return listaProductos
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )

#Leer Producto
def leerProductoPorCodigo(codigoProdu):  
    try:  
        productoEncontrado = []
        with connection.cursor() as cursorConsulta:
            nombreProducto = cursorConsulta.var(cx_Oracle.STRING).var
            marcaProducto= cursorConsulta.var(cx_Oracle.STRING).var
            descripcionProdu = cursorConsulta.var(cx_Oracle.STRING).var
            stockProdu = cursorConsulta.var(cx_Oracle.NUMBER).var
            stockCriticoProdu = cursorConsulta.var(cx_Oracle.NUMBER).var
            fechaVenciProdu = cursorConsulta.var(cx_Oracle.Timestamp).var
            precioProdu = cursorConsulta.var(cx_Oracle.NUMBER).var
            idProveedor = cursorConsulta.var(cx_Oracle.NUMBER).var
            familiaProducto = cursorConsulta.var(cx_Oracle.NUMBER).var
            cursorConsulta.callproc('PRODUCTOPKG.leer_producto', [codigoProdu,nombreProducto,marcaProducto,descripcionProdu,stockProdu,stockCriticoProdu,fechaVenciProdu,precioProdu,idProveedor,familiaProducto])
        productoEncontrado.append(codigoProdu)    
        productoEncontrado.append(nombreProducto.getvalue())            
        productoEncontrado.append(marcaProducto.getvalue()) 
        productoEncontrado.append(descripcionProdu.getvalue())   
        productoEncontrado.append(stockProdu.getvalue())    
        productoEncontrado.append(stockCriticoProdu.getvalue())    
        productoEncontrado.append(fechaVenciProdu.getvalue()) 

        productoEncontrado.append(precioProdu.getvalue())    
        productoEncontrado.append(idProveedor.getvalue())    
        productoEncontrado.append(familiaProducto.getvalue())    

        return productoEncontrado
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )



#Procedimientos almacenados de las ordenes de pedidos. 
#inserta orden de pedido
def insertarOrdenDePedido(fechacodp, estadoodp, precioTotal, fecharodp, rutEmpleado, rutProveedor):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaHuespedBD = cursorConsulta.callfunc('ORDENDEPEDIDOPKG.insertar_ordenpedido',Text,
            [fechacodp, estadoodp, precioTotal, fecharodp, rutEmpleado, rutProveedor])
        return respuestaHuespedBD
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )

#Inserta detalle pedido.
def insertarDetalleDePedido(cantidadProdu, precioPedi,codigoProducto, idOdp):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaHuespedBD = cursorConsulta.callfunc('DETALLEPEDIDOPKG.insertar_detallepedido',Text,
            [cantidadProdu, precioPedi,codigoProducto, idOdp])
        return respuestaHuespedBD
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )

#Para conseguir la ide de la ultima orden de pedido
def conseguirNumeroOPA(rutEmpleado):
    try:
        numeroopa = 0
        with connection.cursor() as cursorConsulta:
            numeroopa = cursorConsulta.var(cx_Oracle.NUMBER).var
            cursorConsulta.callproc('ORDENDEPEDIDOPKG.leer_pedidoactual', [rutEmpleado,numeroopa])
        return numeroopa.getvalue()
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )


#Lista ordenes de pedido por estado
def listarOpPorEstado(estadoOP):
    try:
        listaOrdenesPedido = []

        with connection.cursor() as cursorConsulta:
        #    print(cursorConsulta)
            cursorSalida = cursorConsulta.connection.cursor()
        #    print(cursorSalida)
            cursorConsulta.callproc('ORDENDEPEDIDOPKG.listar_pedidosporestado', [estadoOP, cursorSalida])

        for ordendepedido in cursorSalida:
            listaOrdenesPedido.append(ordendepedido)

        return listaOrdenesPedido
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )

#Elimina la orden de pedido. (Los detalles se eliminan por un trigger en la BD)
def eliminarOP(idOp):    
    try:
        with connection.cursor() as cursorConsulta:
            respuestaEliOp = cursorConsulta.callfunc('ORDENDEPEDIDOPKG.eliminar_ordenpedido', Text,
            [idOp])
        return respuestaEliOp
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )

#Lee una orden de pedido
def leerOrdenPedido(idOp):  
    try:  
        opEncontrada = []
        with connection.cursor() as cursorConsulta:
            fechacodp = cursorConsulta.var(cx_Oracle.Timestamp).var
            estadoodp= cursorConsulta.var(cx_Oracle.NUMBER).var
            precioTotal = cursorConsulta.var(cx_Oracle.NUMBER).var
            fecharodp = cursorConsulta.var(cx_Oracle.Timestamp).var
            rutEmpleado = cursorConsulta.var(cx_Oracle.STRING).var
            rutProveedor = cursorConsulta.var(cx_Oracle.STRING).var
            cursorConsulta.callproc('ORDENDEPEDIDOPKG.leer_ordenpedido', [idOp,fechacodp,estadoodp,precioTotal,fecharodp,rutEmpleado,rutProveedor])
        opEncontrada.append(idOp)    
        opEncontrada.append(fechacodp.getvalue())    
        opEncontrada.append(estadoodp.getvalue()) 
        opEncontrada.append(precioTotal.getvalue())    
        opEncontrada.append(fecharodp.getvalue())    
        opEncontrada.append(rutEmpleado.getvalue())    
        opEncontrada.append(rutProveedor.getvalue())    

        return opEncontrada
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )


#Actualiza una orden de pedido
def actualizarOrdenPedido(idOp,fechacodp,estadoodp,precioTotal,fecharodp,rutEmpleado,rutProveedor):  
    try:  
        with connection.cursor() as cursorConsulta:
            respuestaServBD = cursorConsulta.callfunc('ORDENDEPEDIDOPKG.actualizar_ordenpedido', Text, [idOp,fechacodp,estadoodp,precioTotal,fecharodp,rutEmpleado,rutProveedor])    
        return respuestaServBD
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )


#Procedimiento almacenado para listar los detalles de pedido por orden de pedido.
def listarDetalleOP(idOp):
    try:
        listaProductos = []

        with connection.cursor() as cursorConsulta:
        #    print(cursorConsulta)
            cursorSalida = cursorConsulta.connection.cursor()
        #    print(cursorSalida)
            cursorConsulta.callproc('DETALLEPEDIDOPKG.listar_detallesordendepedido', [idOp, cursorSalida])

        for producto in cursorSalida:
            listaProductos.append(producto)

        return listaProductos
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )

def actualizarDetalleOP(idDetalle,cantidadProdu, precioPedi,codigoProducto, idOdp):  
    try:  
        with connection.cursor() as cursorConsulta:
            respuestaServBD = cursorConsulta.callfunc('DETALLEPEDIDOPKG.actualizar_detallepedido', Text, [idDetalle,cantidadProdu, precioPedi,codigoProducto, idOdp])    
        return respuestaServBD
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

def leerDetalleOP(idDetalle):  
    try:  
        detalleEncontrado = []
        with connection.cursor() as cursorConsulta:
            cantidadProdu = cursorConsulta.var(cx_Oracle.NUMBER).var
            precioPedi= cursorConsulta.var(cx_Oracle.NUMBER).var
            codigoProducto = cursorConsulta.var(cx_Oracle.NUMBER).var
            idOdp = cursorConsulta.var(cx_Oracle.NUMBER).var
            cursorConsulta.callproc('DETALLEPEDIDOPKG.leer_detallepedido', [idDetalle,cantidadProdu,precioPedi,codigoProducto,idOdp])
        detalleEncontrado.append(idDetalle)    
        detalleEncontrado.append(cantidadProdu.getvalue())    
        detalleEncontrado.append(precioPedi.getvalue()) 
        detalleEncontrado.append(codigoProducto.getvalue())    
        detalleEncontrado.append(idOdp.getvalue())    
 

        return detalleEncontrado
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

def eliminarDetalleOP(idDetalle):    
    try:
        with connection.cursor() as cursorConsulta:
            respuestaEliDOp = cursorConsulta.callfunc('DETALLEPEDIDOPKG.eliminar_detallepedido', Text,
            [idDetalle])
        return respuestaEliDOp
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

#Página de ayuda
#Zona de ayuda:
def ayudaempleado(request):
    try:
        return render(request, 'ayudaempleado.html')
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')