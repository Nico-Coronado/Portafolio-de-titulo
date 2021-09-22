from administrador.models import Plato, Comedor
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from apihostal.serializers import PlatoSerializer, ComedorSerializer
from account.models import User
from django.db import connection
from django.utils import timezone
from typing import Text

# Create your views here.
def indexapi(request):
    try:
    #AQUÍ PODEMOS DARLE UN TOKEN A ALGÚN USUARIO. 
        # user = User.objects.get(username='Basti')
        # token = Token.objects.create(user=user)
        # print(token)
        return render(request, 'apihostalclarita.html')
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

# Página de error
def paginaerror(request):
    try:
        return render(request, 'paginaerror.html')
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )

#Página acerca de
def abouthostalclarita(request):
    try:
        return render(request, 'abouthostalclarita.html')
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')

#Página política de privacidad
def politicaprivacidad(request):
    try:
        return render(request, 'politicaprivacidad.html')
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            return redirect('paginaerror')


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]


class PlatoViewSet(viewsets.ModelViewSet):
    try:
        """
        API endpoint that allows groups to be viewed or edited.
        """
        queryset = Plato.objects.all()
        serializer_class = PlatoSerializer
        permission_classes = [permissions.IsAuthenticated]
        #Con esto se pueden definir los parametros.
        def get_queryset(self):
            idComedor = self.request.query_params.get('comedor_id_comedor')
            queryset = Plato.objects.filter(comedor_id_comedor = idComedor)
            return queryset
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )
            
class ComedorViewSet(viewsets.ModelViewSet):
    try:
        """
        API endpoint that allows groups to be viewed or edited.
        """
        queryset = Comedor.objects.all()
        serializer_class = ComedorSerializer
        permission_classes = [permissions.IsAuthenticated]
    except Exception as infoErrorm:
            print("ERROR " + str(infoErrorm) )


def contarVisita(request):
    #Conseguimos el header que contiene la ip
    headerxff = request.META.get('HTTP_X_FORWARDED_FOR')

    if headerxff:
        #Cortamos los proxys por lo que elegimos la primera
        ipVisita = headerxff.split(',')[0]
    else:
        #Si no se encontró ese header, usamos remote_addr que retorna la ip de quien hace el request.
        ipVisita = request.META.get('REMOTE_ADDR')


    fechaActual = timezone.now()
    mensajeIV = insertarVisita(ipVisita,fechaActual)
    return mensajeIV


def insertarVisita(ipvisita,fechavisita):
    try:
        with connection.cursor() as cursorConsulta:
            respuestavisitabd = cursorConsulta.callfunc('VISITAPKG.insertar_visita',Text,
            [ipvisita,fechavisita])
        return respuestavisitabd
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )