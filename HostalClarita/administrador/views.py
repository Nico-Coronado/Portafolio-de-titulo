from cliente.models import Factura
from administrador.models import Habitacion,Comedor, FamiliaProducto, Plato, Moneda
from django.shortcuts import redirect, render
from .forms import comedorLeerform, famipActuForm, famipEliForm, famipLeerForm, platoForm, habitacionForm,comedorForm, comedorActuForm, comedorEliForm, familiaProductoForm,moneForm, monLeerForm,monActuForm,monEliForm
from django.db import connection
from typing import Text
import cx_Oracle
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from datetime import datetime, date
from django.utils import timezone
from empleado.views import leerDetalleOP,leerOrdenPedido,actualizarOrdenPedido,listarDetalleOP,leerProductoPorCodigo,actualizarStockProducto,eliminarOP
from django.contrib import messages
from proveedor.models import Producto



#Portada administrador
def portadaadmin(request):
    try:   
        nombreAdmin = request.user.username
        contexto = {
            'nombreAdmin': nombreAdmin
        }
        return render(request, 'portadaadmin.html', contexto)
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

# HABITACION
def admin_habitacion(request):
    try: 
        if request.method == 'POST': 
            form = habitacionForm(request.POST)
            if form.is_valid():
                numero_de_habitacion = form.cleaned_data['numero_de_habitacion']
                listaHabitaciones = listarHabitaciones()
                for habiBuscada in listaHabitaciones:
                    if numero_de_habitacion == habiBuscada[1]:
                        messages.warning(request, 'Ya existe ese número de habitación.')
                        return redirect('admin-habitacion')

                descripcion_de_la_habitacion = form.cleaned_data['descripcion_de_la_habitacion']
                disponibilidad_habitacion = form.cleaned_data['disponibilidad_habitacion']
                precio = form.cleaned_data['precio']
                mensajeHabiC = print(crearHabitacion(numero_de_habitacion,descripcion_de_la_habitacion,disponibilidad_habitacion,precio))
                mensajeHabiC = "Habitación creada con éxito."
                messages.info(request, mensajeHabiC)
            else:
                messages.warning(request, "No se pudo agregar la habitación, no debe dejar espacios en blanco.")

        data = {'form' : habitacionForm(),
                'lista': listarHabitaciones()}
        return render(request, 'admin_habitacion.html', data )
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

def admin_habitacion_borrar(request,pk):
    try:
        habitacion = Habitacion.objects.get(id=pk)
        if request.method == 'POST':
            mensajeEliHabi = eliminarHabitacion(pk)
            mensajeEliHabi = "Habitación eliminada con éxito."
            messages.info(request, mensajeEliHabi)

            return redirect ('admin-habitacion')
        
        context = {'item': habitacion}
        return render(request, 'admin_habitacion_borrar.html',context )
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

def admin_habitacion_actualizar(request,pk):
    try:
        habitacion = Habitacion.objects.get(id=pk)
        form = habitacionForm(instance=habitacion)
        if request.method == 'POST':
            form = habitacionForm(request.POST, instance=habitacion)
            if form.is_valid():
                numero_de_habitacion = form.cleaned_data['numero_de_habitacion']
                descripcion_de_la_habitacion = form.cleaned_data['descripcion_de_la_habitacion']
                disponibilidad_habitacion = form.cleaned_data['disponibilidad_habitacion']
                precio = form.cleaned_data['precio']
                mensajeActuHabi = print(actualizarHabitacion(pk,numero_de_habitacion,
                descripcion_de_la_habitacion,disponibilidad_habitacion,
                precio))
                mensajeActuHabi = "Habitación actualizada con éxito"
                messages.info(request, mensajeActuHabi)



                return redirect ('admin-habitacion')

        return render(request, 'admin_habitacion_actualizar.html', context={'form': form,
        'item':habitacion})
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')

def crearHabitacion(numero_de_habitacion,descripcion_de_la_habitacion,disponibilidad_habitacion,precio):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaHabitacionBD = cursorConsulta.callfunc('HABITACIONPKG.insertar_habitacion', Text,
            [numero_de_habitacion,descripcion_de_la_habitacion,disponibilidad_habitacion,precio])
        return respuestaHabitacionBD
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )


def eliminarHabitacion(numero_de_habitacion):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaHabitacionBD = cursorConsulta.callfunc('HABITACIONPKG.eliminar_habitacion', Text,
            [numero_de_habitacion])
        return respuestaHabitacionBD
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )


def actualizarHabitacion(id,numero_de_habitacion,descripcion_de_la_habitacion,disponibilidad_habitacion,precio):
    try:    
        with connection.cursor() as cursorConsulta:
            respuestaHabitacionBD = cursorConsulta.callfunc('HABITACIONPKG.actualizar_habitacion', Text,
            [id,numero_de_habitacion,descripcion_de_la_habitacion,disponibilidad_habitacion,precio])
        return respuestaHabitacionBD
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )


def listarHabitaciones():
    try:    
        listaHabitaciones = []

        with connection.cursor() as cursorConsulta:
        #    print(cursorConsulta)
            cursorSalida = cursorConsulta.connection.cursor()
        #    print(cursorSalida)
            cursorConsulta.callproc('HABITACIONPKG.listar_habitaciones', [cursorSalida])

        for habitacion in cursorSalida:
            listaHabitaciones.append(habitacion)

        return listaHabitaciones
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )


# HUESPED
def admin_huesped(request):
    try:    
        context = {'lista':listarHuesped}

        return render(request, 'admin_huesped.html',context)
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')

def listarHuesped():
    try:    
        listaHuesped = []

        with connection.cursor() as cursorConsulta:
        #    print(cursorConsulta)
            cursorSalida = cursorConsulta.connection.cursor()
        #    print(cursorSalida)
            cursorConsulta.callproc('HUESPEDPKG.listar_huespedes', [cursorSalida])

        for habitacion in cursorSalida:
            listaHuesped.append(habitacion)

        return listaHuesped
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )



# COMEDOR Y PLATOS
def admin_plato(request):
    try:   
        if request.method == 'POST':
            form=platoForm(request.POST)
            if form.is_valid():
                nombre_plato = form.cleaned_data['nombre_plato']
                dia_plato = form.cleaned_data['dia_plato']
                hora_plato = form.cleaned_data['hora_plato']            
                precio_plato = form.cleaned_data['precio_plato']           
                comedor_id_comedor = form.cleaned_data['comedor_id_comedor']
                mensajePlatoc = crearPlato(nombre_plato,dia_plato,hora_plato,precio_plato,comedor_id_comedor)
                messages.success(request, mensajePlatoc)
            else:
                messages.warning(request, "Error al agregar plato, no debe dejar espacios vacíos.")


        data = {'form' : platoForm(),
            'listarPlatos' : listarPlatos()}
        return render(request, 'admin_plato.html',data)
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')

def admin_comedor(request):
    try:

        comEncontrado = "Ingrese id para mostrar comedor"
        if request.method == 'POST':
            if 'crear_comedor' in request.POST:
                formInsertar=comedorForm(request.POST)
                if formInsertar.is_valid():
                    nombreC = formInsertar.cleaned_data['servicio_comedor']    
                    mensajeC=crearServcomedor(nombreC)
                    messages.success(request, mensajeC)
                else:
                    messages.warning(request, "No se pudo agregar el comedor, no debe dejar espacios en blancos.")

            formLeer= comedorLeerform(request.POST)
            formActua= comedorActuForm(request.POST)
            formEli= comedorEliForm(request.POST)
            if formLeer.is_valid():
                print('se leyo')
                idComedor= formLeer.cleaned_data['idcomedor']
                comEncontrado = leerServcomedor(idComedor)
                messages.success(request, comEncontrado)
            if 'btnActualizarCom' in request.POST:
                if formActua.is_valid():
                    print('se actualizo')
                    nombreC = formActua.cleaned_data['nomCom']
                    idComedora= formActua.cleaned_data['idcomedora']
                    mensajeC=actualizarServcomedor(idComedora,nombreC)
                    messages.success(request, mensajeC)
                else:
                    messages.warning(request, "No se pudo actualizar el comedor, no debe dejar espacios en blancos.")

            if formEli.is_valid():
                print('se borra')
                idComedore = formEli.cleaned_data['idcomedore']
                mensajeC=eliminarServcomedor(idComedore)
                messages.success(request, mensajeC)
                #Lista de todos los comedores ordenados por el último.
                
        comedores = Comedor.objects.order_by('-id')
        listaComedores = comedores
        comedoresPaginator = Paginator(listaComedores,5)
        print(comedoresPaginator.page(1).object_list)
        numerospagina = request.GET.get('page')
        comedor_objs = comedoresPaginator.get_page(numerospagina)
        #return HttpResponse(crearPlato())
        data = {'form' : comedorForm(),
        'form2': comedorLeerform(),
        'comedorEncontrado': comEncontrado,
        'formActu' : comedorActuForm(),
        'formEli': comedorEliForm(),
        'comedor_objs': comedor_objs}
        return render(request, 'admin_comedor.html',data)
        
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')

def crearPlato(nombreP,diaP,horaP,precioP,servP):
    try:    
        with connection.cursor() as cursorConsulta:
            respuestaPlatoBD = cursorConsulta.callfunc('PLATOPKG.insertar_plato', Text, 
            [nombreP,diaP,horaP,precioP,servP])
        return respuestaPlatoBD
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )

def crearServcomedor(nombreComedor):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaServBD = cursorConsulta.callfunc('COMEDORPKG.insertar_comedor', Text ,[ nombreComedor])
        return respuestaServBD
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )

def leerServcomedor(idComedor):
    try:    
        with connection.cursor() as cursorConsulta:
            descripcion = cursorConsulta.var(cx_Oracle.STRING).var
            cursorConsulta.callproc('COMEDORPKG.leer_comedor', [idComedor,descripcion])
        if descripcion.getvalue() == None: return 'No se encontro el comedor' 
        return 'Id comedor: ' + str(idComedor) + ', Nombre Servicio: ' + descripcion.getvalue()
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
        
def listarComedor():
    try:
        listaComedor = []
        with connection.cursor() as cursorConsulta:
        #    print(cursorConsulta)
            cursorSalida = cursorConsulta.connection.cursor()
        #    print(cursorSalida)
            cursorConsulta.callproc('COMEDORPKG.listar_comedores', [cursorSalida])

        for comedor in cursorSalida:
            listaComedor.append(comedor)

        return listaComedor
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
           
def actualizarServcomedor(idComedor, nombreComedor):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaServBD = cursorConsulta.callfunc('COMEDORPKG.actualizar_comedor', Text,[idComedor, nombreComedor])
        return respuestaServBD
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
      

def eliminarServcomedor(idComedor):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaServBD = cursorConsulta.callfunc('COMEDORPKG.eliminar_comedor',Text,[idComedor])
        return respuestaServBD
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
    

def admin_Servcomedor_borrar(request,pk):
    try:
        comedor =Comedor.objects.get(id=pk)
        if request.method == 'POST':
            eliminarServcomedor(pk)
            return redirect('admin_comedor')

        context = {'item': comedor}
        return render(request, 'admin_habitacion_borrar.html',context )
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')

def admin_Servcomedor_actualizar(request,pk):
    try:
        comedor = Comedor.objects.get(id=pk)
        form = comedorForm(instance=comedor)
        if request.method == 'POST':
            form = comedorForm(request.POST, instance=comedor)
            if form.is_valid():           
                Servcomedor =form.cleaned_data['servicio_comedor'] 
                print(actualizarServcomedor(comedor,Servcomedor))           
                return redirect ('admin_comedor.html')

        return render(request, 'admin_habitacion_actualizar.html', context={'form': form,
        'item':comedor})
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')

def adminComedorleer(request):
    try:
        form= comedorLeerform()           
        return redirect( 'admin_comedor.html')
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')

def eliminarPlato(nombre_plato):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaPlatoBD = cursorConsulta.callfunc('PLATOPKG.eliminar_plato', Text,
            [nombre_plato])
        return respuestaPlatoBD
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
   
def actualizarPlato(idplato,nombre_plato,dia_plato,hora_plato,precio_plato):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaPlatoBD = cursorConsulta.callfunc('PLATOPKG.actualizar_plato', Text,
            [idplato,nombre_plato,dia_plato,hora_plato,precio_plato])
        return respuestaPlatoBD
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )

def leerplato(id_plato):
    try:
        with connection.cursor() as cursorConsulta:
            nombre_plato = cursorConsulta.var(cx_Oracle.STRING).var
            dia_plato= cursorConsulta.var(cx_Oracle.NUMBER).var
            hora_plato = cursorConsulta.var(cx_Oracle.STRING).var
            precio_plato = cursorConsulta.var(cx_Oracle.NUMBER).var
            comedor_id_comedor = cursorConsulta.var(cx_Oracle.NUMBER).var
            cursorConsulta.callproc('PLATOPKG.leer_plato', [id_plato,nombre_plato,dia_plato,hora_plato,precio_plato,comedor_id_comedor])
        return 'Id comedor: ' + str(id_plato) + ', Nombre Plato: ' + nombre_plato.getvalue() + 'Dia del Plato: ' + str(dia_plato.getvalue()) + 'Hora del plato: ' + (hora_plato).getvalue() + 'Precio del Plato: ' + str(precio_plato.getvalue()) + 'Comedor: ' + str(comedor_id_comedor.getvalue())
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
  
# Listar de plato
def listarPlatos():
    try:
        listaPlatos = []
        with connection.cursor() as cursorConsulta:
        #    print(cursorConsulta)
            cursorSalida = cursorConsulta.connection.cursor()
        #    print(cursorSalida)
            cursorConsulta.callproc('PLATOPKG.listar_platos', [cursorSalida])

        for platos in cursorSalida:
            listaPlatos.append(platos)

        return listaPlatos
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
  
def plato_eli(request,pk):
    try:
        platoE =Plato.objects.get(id=pk)
        if request.method == 'POST':
            mensajeElip = eliminarPlato(pk)
            messages.info(request, mensajeElip)

            return redirect('admin-plato')
        
        context = {'item': platoE}
        return render(request, 'admin_plato_eli.html',context )
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')

def plato_actu(request,pk):
    try:
        plato= Plato.objects.get(id=pk)
        
        form = platoForm(instance=plato)
        if request.method == 'POST':
            form = platoForm(request.POST, instance=plato)
            if form.is_valid():
                nombre_plato = form.cleaned_data['nombre_plato']
                dia_plato = form.cleaned_data['dia_plato']
                hora_plato = form.cleaned_data['hora_plato']
                precio_plato = form.cleaned_data['precio_plato']
                
                mensajeActup = actualizarPlato(pk,nombre_plato,dia_plato,hora_plato,precio_plato)
                messages.info(request, mensajeActup)



                return redirect('admin-plato')
        return render(request,'admin_plato_actu.html', context={'form': form,'item':plato})
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')

def productFam(request):
    try:


        productFame="Ingrese id para mostrar la familia del producto"
        if request.method == 'POST':
            form=familiaProductoForm(request.POST)
            formLeer=famipLeerForm(request.POST)        
            formActua=famipActuForm(request.POST)        
            formEli=famipEliForm(request.POST)
            if 'btnAgregarFamilia' in request.POST:
                if form.is_valid():
                    nombre_familiap=form.cleaned_data['nombre_familiap'] 
                    mensajeC=crearProductoFam(nombre_familiap)
                    messages.success(request,mensajeC)
                else:
                    messages.warning(request, "Error al agregar familia de productos, no debe dejar espacios vacíos.")
            if formLeer.is_valid():
                id = formLeer.cleaned_data['idl']
                mensajefpl = productFame=leerProductoFam(id)
                mensajefpl = "Familia de producto encontrada con éxito."
                messages.success(request,mensajefpl)
            if 'btnActuFamilia' in request.POST:
                if formActua.is_valid():
                    id = formActua.cleaned_data['ida']
                    nombre_familiap = formActua.cleaned_data['nombre_familiap']
                    mensajeC=actualizarProductoFam(id, nombre_familiap)
                    messages.success(request,mensajeC)
                else:
                    messages.warning(request, "Error al actualizar familia de productos, no debe dejar espacios vacíos.")
            
            if formEli.is_valid():
                id = formEli.cleaned_data['ide']
                mensajeC=eliminarProductoFam(id)
                messages.info(request,mensajeC)        
        #Lista de todas las familias de productos ordenadas por la última.
        familiaproductos = FamiliaProducto.objects.order_by('-id')
        listaFamiliasProdu = familiaproductos
        familiapPaginator = Paginator(listaFamiliasProdu,5)
        print(familiapPaginator.page(1).object_list)
        numerosPagina = request.GET.get('page')
        familiaprod_objs = familiapPaginator.get_page(numerosPagina)

        data = {'form' : familiaProductoForm(),
                'formLeer' : famipLeerForm(),
                'formActua':famipActuForm(),            
                'formEli': famipEliForm(),
                'productFame' : productFame,
                'familiaprod_objs':familiaprod_objs}
        return render(request, 'admin_familiaproducto.html',data)
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')

def crearProductoFam(nombre_familiap):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaServBD = cursorConsulta.callfunc('FAMILIAPRODUCTOPKG.insertar_familiaprod', Text ,[ nombre_familiap])
        return respuestaServBD
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
      
def leerProductoFam(id_familiap):
    try:
        with connection.cursor() as cursorConsulta:
            descripcion = cursorConsulta.var(cx_Oracle.STRING).var
            cursorConsulta.callproc('FAMILIAPRODUCTOPKG.leer_familiaprod', [id_familiap,descripcion])
        if descripcion.getvalue() == None: return 'No se encontro el producto' 
        return 'Id Familia producto: ' + str(id_familiap) + ', Nombre Producto: ' + descripcion.getvalue()
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
        
def actualizarProductoFam(id_familiap,nombre_familiap):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaServBD = cursorConsulta.callfunc('FAMILIAPRODUCTOPKG.actualizar_familiaprod', Text,[id_familiap, nombre_familiap])
        return respuestaServBD
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
     
def eliminarProductoFam(id_familiap):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaServBD = cursorConsulta.callfunc('FAMILIAPRODUCTOPKG.eliminar_familiaprod',Text,[id_familiap])
        return respuestaServBD
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
  
def moneda(request):
    try:

        productFame="Ingrese id para mostrar el codigo de la moneda"
        if request.method == 'POST':
            if 'crear_moneda' in request.POST:    
                form=moneForm(request.POST)
                if form.is_valid():
                    codigo_moneda=form.cleaned_data['codigo_moneda'] 
                    valor_peso=form.cleaned_data['valor_peso']
                    mensajeC=crearMoneda(codigo_moneda,valor_peso)
                    messages.success(request,mensajeC)
                else:
                    messages.warning(request, "Error al agregar a la moneda, no debe dejar espacios vacíos.")

            formLeer=monLeerForm(request.POST)        
            formActua=monActuForm(request.POST)        
            formEli=monEliForm(request.POST)
            
                
            if formLeer.is_valid():
                id = formLeer.cleaned_data['idl']
                monedaFame=leerMoneda(id)
                messages.info(request,monedaFame)
            if 'btnActuMon' in request.POST:   
                if formActua.is_valid():
                        ida = formActua.cleaned_data['ida']
                        codigo_monedaa = formActua.cleaned_data['codigo_moneda']
                        valor_pesoa = formActua.cleaned_data['valor_pesoa']
                        mensajeC=actualizarMoneda(ida, codigo_monedaa,valor_pesoa)
                        messages.success(request,mensajeC)
                else:
                    messages.warning(request, "Error al actualizar a la moneda, no debe dejar espacios vacíos.")

            if formEli.is_valid():
                id = formEli.cleaned_data['ide']
                mensajeC=eliminarMoneda(id)
                messages.info(request,mensajeC)        
               #Lista de todas las monedas ordenadas por la última.
        monedas = Moneda.objects.order_by('-id')
        listaMonedas = monedas
        monedasPaginator = Paginator(listaMonedas,5)
        print(monedasPaginator.page(1).object_list)
        numerosPagina = request.GET.get('page')
        moneda_objs = monedasPaginator.get_page(numerosPagina)

        data = {'form' : moneForm(),
                'formLeer' : monLeerForm(),
                'formActua':monActuForm(),            
                'formEli': monEliForm   (),
                'productFame' : productFame,
                'moneda_objs': moneda_objs}
        return render(request, 'admin_moneda.html',data)
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')

def crearMoneda(codigo_moneda,valor_peso):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaServBD = cursorConsulta.callfunc('MONEDAPKG.insertar_moneda', Text ,[ codigo_moneda,valor_peso])
        return respuestaServBD
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
  

def leerMoneda(id_moneda):
    try:
        with connection.cursor() as cursorConsulta:
            codigo_moneda = cursorConsulta.var(cx_Oracle.STRING).var
            valor_peso = cursorConsulta.var(cx_Oracle.NUMBER).var
            cursorConsulta.callproc('MONEDAPKG.leer_moneda', [id_moneda,codigo_moneda,valor_peso])
        if codigo_moneda.getvalue() == None: return 'No se encontro la moneda' 
        return 'Id Moneda: ' + str(id_moneda) + ', Nombre moneda: ' + codigo_moneda.getvalue() + ',el valor del peso es: ' + str(valor_peso.getvalue())
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
    
def actualizarMoneda(id_moneda,codigo_moneda,valor_peso):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaServBD = cursorConsulta.callfunc('MONEDAPKG.actualizar_moneda', Text,[id_moneda,codigo_moneda,valor_peso])
        return respuestaServBD
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
        
def eliminarMoneda(id_moneda):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaServBD = cursorConsulta.callfunc('MONEDAPKG.eliminar_moneda',Text,[id_moneda])
        return respuestaServBD  
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
      

def admin_pedidos(request):
    try:
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

        if 'btnEliminarPedido' in request.POST:
            opNoDeseado = int(request.POST.get('btnEliminarPedido'))
            print(eliminarOP(opNoDeseado))

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


        if 'btnAceptarProductos' in request.POST:
            idOpAceptada = int(request.POST.get('btnAceptarProductos'))
            opAceptada = leerOrdenPedido(idOpAceptada)
            print(actualizarOrdenPedido(opAceptada[0],opAceptada[1],5,opAceptada[3],opAceptada[4],opAceptada[5],opAceptada[6])) 


        pedidosCreados = listarPedidos()
        contexto = {'listaPedidosCreados' : pedidosCreados,}
        return render(request, 'admin_pedidos.html',contexto)
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')

def admin_facturas(request):
    try:
        return render(request,'admin_facturas.html',context={'facturas':listarFactura()})
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')

def admin_facturas_borrar(request,pk):
    try:
        factura = Factura.objects.get(pk=pk)
        if request.method == 'POST':
            eliminarFactura(pk)
            return redirect ('admin-facturas')
        
        context = {'item': factura}
        return render(request,'admin_facturas_borrar.html',context)
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')


def listarPedidos():
    try:    
        listaPedidos = []

        with connection.cursor() as cursorConsulta:
        #    print(cursorConsulta)
            cursorSalida = cursorConsulta.connection.cursor()
        #    print(cursorSalida)
            cursorConsulta.callproc('ORDENDEPEDIDOPKG.listar_ordenespedidos', [cursorSalida])

        for pedido in cursorSalida:
            listaPedidos.append(pedido)

        return listaPedidos
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )

def listarProductos():
    try:    
        listaProductos = []

        with connection.cursor() as cursorConsulta:
        #    print(cursorConsulta)
            cursorSalida = cursorConsulta.connection.cursor()
        #    print(cursorSalida)
            cursorConsulta.callproc('PRODUCTOPKG.listar_productos', [cursorSalida])

        for producto in cursorSalida:
            listaProductos.append(producto)

        return listaProductos
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )

def eliminarFactura(numeroFactura):
    try:
        with connection.cursor() as cursorConsulta:
            respuestaHabitacionBD = cursorConsulta.callfunc('facturapkg.eliminar_factura', Text,
            [numeroFactura])
        return respuestaHabitacionBD
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )

def listarFactura():
    try:
        listaFactura = []

        with connection.cursor() as cursorConsulta:
        #    print(cursorConsulta)
            cursorSalida = cursorConsulta.connection.cursor()
        #    print(cursorSalida)
            cursorConsulta.callproc('FACTURAPKG.listar_facturas', [cursorSalida])

        for habitacion in cursorSalida:
            listaFactura.append(habitacion)

        return listaFactura
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
        

#Zona de estadisticas
def admin_estadistica(request):
    try:
        listaEstadisticas = []
        fechaActual = timezone.now()

        #Zona visitas a la página web.
        visitasDelMes = 0
        visitasAnuales = 0
        visitasMesIP = 0
        visitasAnualIP = 0

        #Zona Ganancias
        facturasDelMes =0
        facturasAnuales = 0
        totalGanadoMes =0
        totalGanadoAnual =0

        #Zona Gastos
        pedidosDelMes = 0
        pedidosAnuales = 0
        totalGastadoMes = 0
        totalGastadoAnual = 0

        with connection.cursor() as cursor:

            #CONTADOR DE VISITAS DEL MES.
            cursor.execute("SELECT COUNT(*) FROM apihostal_visita WHERE EXTRACT(MONTH FROM fechavisita)=%s AND EXTRACT(year from fechavisita)=%s", [str(fechaActual.month),str(fechaActual.year)])
            visitasDelMes = cursor.fetchone()
            print('VISITAS DEL MES: ' + str(visitasDelMes[0]))
            #CONTADOR DE VISITAS DEL AÑO.
            cursor.execute("SELECT COUNT(*) FROM apihostal_visita WHERE EXTRACT(year from fechavisita)=%s;", [str(fechaActual.year)])
            visitasAnuales = cursor.fetchone()
            print('Visitas DEL AÑO: ' + str(visitasAnuales[0]))
            #TOTAL MES FILTRADO IP
            cursor.execute("SELECT count(ipvisita) FROM apihostal_visita WHERE EXTRACT(MONTH FROM fechavisita)=%s AND EXTRACT(year from fechavisita)=%s ORDER BY id;", [str(fechaActual.month),str(fechaActual.year)])
            visitasMesIP = cursor.fetchone()
            print('VISITAS DEL MES POR IP: ' + str(visitasMesIP[0]))
            #TOTAL AÑO FILTRADO IP
            cursor.execute("SELECT COUNT(ipvisita) FROM apihostal_visita WHERE EXTRACT(year from fechavisita)=%s ORDER BY id;", [str(fechaActual.year)])
            visitasAnualIP = cursor.fetchone()
            print('Visitas DEL AÑO POR IP: ' + str(visitasAnualIP[0]))

            #CONTADOR DE FACTURAS GENERADAS EN EL MES.        
            cursor.execute("SELECT COUNT(codigo_factura) FROM cliente_factura WHERE EXTRACT(MONTH FROM fecha_emision)=%s AND EXTRACT(year from fecha_emision)=%s;", [str(fechaActual.month),str(fechaActual.year)])
            facturasDelMes = cursor.fetchone()
            print('FACTURAS DEL MES: ' + str(facturasDelMes[0]))
            
            #CONTADOR DE FACTURAS GENERADAS EN EL AÑO.
            cursor.execute("SELECT COUNT(codigo_factura) FROM cliente_factura WHERE EXTRACT(year from fecha_emision)=%s;", [str(fechaActual.year)])
            facturasAnuales = cursor.fetchone()
            print(f"FACTURAS DEL AÑO: {facturasAnuales[0]}")


            #CONTADOR DE GANANCIA DE FACTURAS EN EL MES.
            cursor.execute("SELECT SUM(precio_total) FROM cliente_factura WHERE EXTRACT(MONTH FROM fecha_emision)=%s AND EXTRACT(year from fecha_emision)=%s;", [str(fechaActual.month),str(fechaActual.year)])
            totalGanadoMes = cursor.fetchone()
            print(f"GANANCIA DEL MES: {totalGanadoMes[0]}")

            #CONTADOR DE GANANCIA DE FACTURAS EN EL AÑO.
            cursor.execute("SELECT SUM(precio_total) FROM cliente_factura WHERE EXTRACT(year from fecha_emision)=%s;", [str(fechaActual.year)])
            totalGanadoAnual = cursor.fetchone()
            print(f"GANANCIA DEL AÑO: {totalGanadoAnual[0]}")            

            #CONTADOR DE PEDIDOS GENERADOS EN EL MES.
            cursor.execute("SELECT COUNT(id) FROM empleado_ordenpedido WHERE EXTRACT(MONTH FROM fecha_rodp)=%s AND EXTRACT(year from fecha_rodp)=%s AND estado_odp = %s;", [str(fechaActual.month),str(fechaActual.year), 5])
            pedidosDelMes = cursor.fetchone()
            print(f"PEDIDOS DEL MES: {pedidosDelMes[0]}")    

            #CONTADOR DE PEDIDOS GENERADOS EN EL AÑO.
            cursor.execute(" SELECT COUNT(id) FROM empleado_ordenpedido WHERE EXTRACT(year from fecha_rodp)=%s AND estado_odp = %s;", [str(fechaActual.year), 5])
            pedidosAnuales = cursor.fetchone()
            print(f"PEDIDOS DEL AÑO: {pedidosAnuales[0]}")            

            #CONTADOR DE GASTOS DE PROVEEDORES EN EL MES.            
            cursor.execute("SELECT SUM(precio_total_odp) FROM empleado_ordenpedido WHERE EXTRACT(MONTH FROM fecha_rodp)=%s AND EXTRACT(year from fecha_rodp)=%s AND estado_odp = %s;", [str(fechaActual.month),str(fechaActual.year), 5])
            totalGastadoMes = cursor.fetchone()
            print(f"GASTADO DEL MES: {totalGastadoMes[0]}")            


            #CONTADOR DE GASTOS DE PROVEEDORES EN EL AÑO.           
            cursor.execute(" SELECT SUM(precio_total_odp) FROM empleado_ordenpedido WHERE EXTRACT(year from fecha_rodp)=%s AND estado_odp = %s;", [str(fechaActual.year), 5])
            totalGastadoAnual = cursor.fetchone()
            print(f"GASTADO DEL AÑO: {totalGastadoAnual[0]}")   

        contexto = {'visitasDelMes': visitasDelMes,
                    'visitasAnuales': visitasAnuales,
                    'visitasMesIP': visitasMesIP,
                    'visitasAnualIP': visitasAnualIP,
                    'facturasDelMes': facturasDelMes,
                    'facturasAnuales':facturasAnuales,
                    'totalGanadoMes':totalGanadoMes,
                    'totalGanadoAnual':totalGanadoAnual,
                    'pedidosDelMes':pedidosDelMes,
                    'pedidosAnuales':pedidosAnuales,
                    'totalGastadoMes':totalGastadoMes,
                    'totalGastadoAnual':totalGastadoAnual,
                    'fechaActual': fechaActual}

        return render(request, 'admin_estadistica.html', contexto)
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')


def huespedesactuales(request):
    try:
        context = {'lista':listarHuespedesa(1)}

        return render(request, 'admin_huespedesa.html',context)
        

    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')



def listarHuespedesa(estadoh):
    try:
        listaHabitaciones = []

        with connection.cursor() as cursorConsulta:
        #    print(cursorConsulta)
            cursorSalida = cursorConsulta.connection.cursor()
        #    print(cursorSalida)
            cursorConsulta.callproc('HUESPEDPKG.listar_estadohuespedes', [estadoh,cursorSalida])

        for habitacion in cursorSalida:
            listaHabitaciones.append(habitacion)

        return listaHabitaciones
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )


#Ayuda de Admin 
def ayudaadministrador(request):
    try:
        return render(request, 'ayudaadministrador.html')
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')


#Mostrar productos
def mostrarProductos(request):
    try:
        productos = listarProductos()
        return render(request,'admin_listar_productos.html',context={'lista':productos})
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')


#Sistema de hostal.
def sistemahostal(request):
    try:

        if "btnActualizarHostal" in request.POST:
            #Revisamos las reservas.
            #2: HUESPED EN RESERVA
            listaReservas = listarHuespedesa(2)
            print(str(listaReservas))
            tiempoActual = date.today()
            huespedesLiberados = 0
            huespedesIngresados = 0
            for huesped in listaReservas:
                print(huesped[3].date())
                print(tiempoActual)
                if huesped[3].date() == tiempoActual:
                    #1: HuespedActivo
                    actualizarestHuesped(huesped[0],1)
                    #ASIGNAMOS LAS HABITACIONES 
                    #2: ESTAR ASIGNADO A EMPRESA
                    actualizarestHabi(int(huesped[6]),2)
                    huespedesIngresados = huespedesIngresados + 1
                elif huesped[4].date() == tiempoActual:
                    #0: HuespedInactivo
                    actualizarestHuesped(huesped[0],0)
                    #ASIGNAMOS LAS HABITACIONES 
                    #0: DISPONIBLE.
                    actualizarestHabi(int(huesped[6]),0)
                    huespedesLiberados = huespedesLiberados + 1
        
            messages.success(request, "Se han ingresado: " + str(huespedesIngresados) + " huéspedes. Se han liberado: " + str(huespedesLiberados) + " huéspedes.")
            print("HUespedes ingresado: " + str(huespedesIngresados))
        return render(request,'sistemahostal.html')
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')


def actualizarestHuesped(idhuesped,estadohuesped):
    try:    
        with connection.cursor() as cursorConsulta:
            respuestaeHuespedBD = cursorConsulta.callfunc('HUESPEDPKG.actualizar_estadohue', Text,
            [idhuesped, estadohuesped])
        return respuestaeHuespedBD
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )


def actualizarestHabi(numerohabi, disponibilidadh):
    try:    
        with connection.cursor() as cursorConsulta:
            respuestaeHabitacionBD = cursorConsulta.callfunc('HABITACIONPKG.actualizar_estadohabi', Text,
            [numerohabi, disponibilidadh])
        return respuestaeHabitacionBD
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm))