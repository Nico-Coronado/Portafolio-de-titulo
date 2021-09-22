from administrador.views import actualizarHabitacion
from proveedor.models import Producto
from django.shortcuts import redirect, render
from .forms import productoForm
from django.db import connection
from typing import Text
from account.models import Proveedor, Empleado
from django.utils import timezone
import cx_Oracle
from django.contrib import messages

#Página principal proveedor
def proveedor(request):
    try:
        if(request.user.is_superuser):
            nombreProveedor = request.user.username
        else:
            nombreProveedor = request.user.proveedor.nombre_proveedor
        
        contexto = {
            'nombreProveedor': nombreProveedor
        }
        return render(request, 'proveedor.html', contexto)
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')



# PRODUCTO
def crearproducto(request):
    try:
      #  if 'btnBorrarProducto' in request.POST:

        if request.method == 'POST': 
            form = productoForm(request.POST)
            if form.is_valid():
                nombre_del_producto = form.cleaned_data['nombre_del_producto']
                marca_del_producto = form.cleaned_data['marca_del_producto']
                descripcion_del_producto = form.cleaned_data['descripcion_del_producto']
                stock = form.cleaned_data['stock']
                stock_critico = form.cleaned_data['stock_critico']
                fecha_de_vencimiento = form.cleaned_data['fecha_de_vencimiento']
                precio = form.cleaned_data['precio']
                id_proveedor = request.user
                familia_producto = form.cleaned_data['familia_producto']
                mensajeProductoc = crearProducto(nombre_del_producto,marca_del_producto,descripcion_del_producto,
                                    stock,stock_critico,fecha_de_vencimiento,precio,id_proveedor.id,
                                    familia_producto.id)
                messages.info(request, mensajeProductoc)  

        context = {'form': productoForm(),
                'lista': listarProductoDeProveedor(request.user.id)}
        return render(request, 'proveedor_producto.html',context)

    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

def crearProducto(nombre_del_producto,marca_del_producto,descripcion_del_producto,
                 stock, stock_critico, fecha_de_vencimiento, precio, id_proveedor, familia_producto):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaProductoBD = cursorConsulta.callfunc('PRODUCTOPKG.insertar_producto', Text,
            [nombre_del_producto,marca_del_producto,descripcion_del_producto,stock,stock_critico,
            fecha_de_vencimiento,precio,id_proveedor,familia_producto])
        return respuestaProductoBD
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
    

def producto_borrar(request,pk):
    try:
        producto = Producto.objects.get(id=pk)
        if request.method == 'POST':
            mensajeEliProd = eliminarProducto(pk)
            mensajeEliProd = "Producto eliminado con éxito."
            messages.info(request, mensajeEliProd)  

            return redirect('crearproducto')

        context = {'item':producto}
        return render(request,'producto_borrar.html',context)
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

def producto_actualizar(request,pk):
    try:
        producto = Producto.objects.get(id=pk)
        form = productoForm(instance=producto)
        if request.method == 'POST':
            form = productoForm(request.POST, instance=producto)
            if form.is_valid():
                nombre_del_producto = form.cleaned_data['nombre_del_producto']
                marca_del_producto = form.cleaned_data['marca_del_producto']
                descripcion_del_producto = form.cleaned_data['descripcion_del_producto']
                stock = form.cleaned_data['stock']
                stock_critico = form.cleaned_data['stock_critico']
                fecha_de_vencimiento = form.cleaned_data['fecha_de_vencimiento']
                precio = form.cleaned_data['precio']
                familia_producto = form.cleaned_data['familia_producto']
                mensajeActuProd= actualizarProducto(pk,nombre_del_producto,marca_del_producto,descripcion_del_producto,
                stock,stock_critico,fecha_de_vencimiento,precio,familia_producto.id)

                mensajeActuProd = "Producto actualizado con éxito."
                messages.info(request, mensajeActuProd)  

                return redirect('crearproducto')

        return render(request,"producto_actualizar.html",context={'form': form,'item':producto})
        
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

def eliminarProducto(idproducto):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaProductoBD = cursorConsulta.callfunc('PRODUCTOPKG.eliminar_producto',Text,
            [idproducto])
        return respuestaProductoBD
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
    

def actualizarProducto(id,nombre_del_producto,marca_del_producto,descripcion_del_producto,
                 stock, stock_critico, fecha_de_vencimiento, precio, familia_producto):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaProductoBD = cursorConsulta.callfunc('PRODUCTOPKG.actualizar_producto',Text,[id,nombre_del_producto,marca_del_producto,descripcion_del_producto,
                    stock, stock_critico, fecha_de_vencimiento, precio, familia_producto])
        return respuestaProductoBD
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )


def listarProducto():
    try:
        listaProductos = []

        with connection.cursor() as cursorConsulta:
            cursorSalida = cursorConsulta.connection.cursor()
            cursorConsulta.callproc('PRODUCTOPKG.listar_productos',[cursorSalida])
        for producto in cursorSalida:
            listaProductos.append(producto)
        return listaProductos
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')


#Lista de ordenes de pedido pendientes
def proveedor_lista(request):
    try:
            # ESTADOS DE ORDEN DE PEDIDO
            # 0: creados.
            # 1: pendiente.
            # 2: entregada:
            # 3: rechazada.
            # 4: cancelada.
            # 5: aceptada.
        if(request.user.is_superuser):
            listaMisPedidos = listarPedidosProv("71369625-0",1)
        else:
            listaMisPedidos = listarPedidosProv(str(request.user.proveedor.rut),1)

        if 'btnEnviarProductos' in request.POST:
                idEnviarOP = int(request.POST.get('btnEnviarProductos'))
                #VALIDAR STOCK STOCK
                listaDetallesOP = listarDetalleOP(idEnviarOP)
                stockSuperado = False
                productoSuperado = ''
                stockActualProducto = 0
                for detalleValidacion in listaDetallesOP:
                    # detalleEncontrado.append(idDetalle)    
                    # detalleEncontrado.append(cantidadProdu.getvalue())    
                    # detalleEncontrado.append(precioPedi.getvalue()) 
                    # detalleEncontrado.append(codigoProducto.getvalue())    
                    # detalleEncontrado.append(idOdp.getvalue())
                    productoSuperaStock =  leerProductoPorCodigo(detalleValidacion[3])
                    if  0 > (productoSuperaStock[4] - detalleValidacion[1]):
                        stockSuperado = True
                        productoSuperado = productoSuperaStock[1]
                        stockActualProducto = productoSuperaStock[4]
                        break
                if stockSuperado:
                    messages.error(request, "No se puede enviar el pedido, se supera el stock del producto: "+ str(productoSuperado) + ", Stock Actual: " + str(round(stockActualProducto)))

                    return redirect('proveedor-lista')
                
                        
                opPreparada = leerOrdenPedido(int(idEnviarOP))
                tiempoActual = timezone.now()
                print(actualizarOrdenPedido(opPreparada[0],tiempoActual,2,opPreparada[3],opPreparada[4],opPreparada[5],opPreparada[6]))

                if(request.user.is_superuser):
                    listaMisPedidos = listarPedidosProv("71369625-0",1)
                else:
                    listaMisPedidos = listarPedidosProv(str(request.user.proveedor.rut),1)

                #ACTUALIZAR STOCK
                for detalleConsulta in listaDetallesOP:
                    # detalleEncontrado.append(idDetalle)    
                    # detalleEncontrado.append(cantidadProdu.getvalue())    
                    # detalleEncontrado.append(precioPedi.getvalue()) 
                    # detalleEncontrado.append(codigoProducto.getvalue())    
                    # detalleEncontrado.append(idOdp.getvalue())
                    productoEncontrado =  leerProductoPorCodigo(detalleConsulta[3])
                    actualizarStockProducto(detalleConsulta[3],(productoEncontrado[4] - detalleConsulta[1]))                  
                #Mensade de éxito:
                messages.success(request, "Pedido envíado con éxito.")  
        if 'btnCancelarPedido' in request.POST:
                idCancelarOp = int(request.POST.get('btnCancelarPedido'))
                opCancelada = leerOrdenPedido(int(idCancelarOp))
                print(actualizarOrdenPedido(opCancelada[0],opCancelada[1],4,opCancelada[3],opCancelada[4],opCancelada[5],opCancelada[6]))

                if(request.user.is_superuser):
                    listaMisPedidos = listarPedidosProv("71369625-0",1)
                else:
                    listaMisPedidos = listarPedidosProv(str(request.user.proveedor.rut),1)
                messages.success(request, "Pedido cancelado con éxito.")  

        
        contexto = {'listaMisPedidos':listaMisPedidos}
        return render(request, 'proveedor_lista.html',contexto)
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

#View para ver los pedidos
def mostrarpedidop(request):
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
            datosProveedor = proveedorOP.nombre_proveedor + ' Rut:' + proveedorOP.rut 

            solicitanteOP = Empleado.objects.filter(rut=str(ordenPedidoConsulta[5])).first()
            if(solicitanteOP != None):
                datosSolicitante = solicitanteOP.nombre_completo_empleado + ' Rut:' +   solicitanteOP.rut 
            else:
                datosSolicitante = "ADMINISTRADOR HOSTAL CLARITA"
                
        contexto = {'listaProductosOP': listaProductosOP,
        'numeroOrden': numeroOrden,
        'fechaCreacion': fechaCreacion,
        'precioTotal': precioTotal,
        'datosSolicitante':datosSolicitante,
        'datosProveedor': datosProveedor}


        return render(request, 'mostrar_pedidop.html',contexto)

    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

#Historial de todos los pedidos 
def historialpedidosp(request):
    try:
        #PEDIDOS
        # 0: creados.
        # 1: pendiente.
        # 2: entregada:
        # 3: rechazada.
        # 4: cancelada.
        # 5: aceptada.
        
        if(request.user.is_superuser):
            lpedidosAceptados = listarPedidosProv("71369625-0",5)
            lpedidosRechazados  = listarPedidosProv("71369625-0",3)
            lpedidosEntregados =  listarPedidosProv("71369625-0",2)
            lpedidosCancelados = listarPedidosProv("71369625-0",4)        
        else:
            lpedidosAceptados = listarPedidosProv(str(request.user.proveedor.rut),5)
            lpedidosRechazados  = listarPedidosProv(str(request.user.proveedor.rut),3)
            lpedidosEntregados =  listarPedidosProv(str(request.user.proveedor.rut),2)
            lpedidosCancelados = listarPedidosProv(str(request.user.proveedor.rut),4)

        contexto = {'lpedidosAceptados':lpedidosAceptados,
                'lpedidosRechazados':lpedidosRechazados,
                'lpedidosEntregados':lpedidosEntregados,
                'lpedidosCancelados':lpedidosCancelados }

        return render(request, 'historial_pedidosp.html',contexto)
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')




#Actualizar stock de producto


def actualizarStockProducto(codigoProducto,stock):  
    try:  
        if(stock < 0):
            stock = 0
        with connection.cursor() as cursorConsulta:
            respuestaServBD = cursorConsulta.callfunc('PRODUCTOPKG.actualizar_stockproducto', Text, [codigoProducto,stock])    
        return respuestaServBD
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

#Para leer ordenes de pedido
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



def listarProductoDeProveedor(idProveedor):
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
        
#lista de pedidos pendientes del proveedor y su estado.
def listarPedidosProv(rutProveedor, estadoOp):
    try:
        listaOrdenesPedido = []

        with connection.cursor() as cursorConsulta:
        #    print(cursorConsulta)
            cursorSalida = cursorConsulta.connection.cursor()
        #    print(cursorSalida)
            cursorConsulta.callproc('ORDENDEPEDIDOPKG.listar_pedidosproveedor', [rutProveedor,estadoOp, cursorSalida])

        for ordendepedido in cursorSalida:
            listaOrdenesPedido.append(ordendepedido)

        return listaOrdenesPedido
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )

#Zona de ayuda proveedor:
def ayudaproveedor(request):
    try:
        return render(request, 'ayudaproveedor.html')
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')