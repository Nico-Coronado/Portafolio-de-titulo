from django.urls import path
from .import views

urlpatterns = [
    path('', views.empleado, name="empleado"),
    path('crearpedido', views.crearpedido, name="crearpedido"),
    path('mostrarpedidonuevo', views.mostrarpedidonuevo, name="mostrarpedidonuevo"),
    path('administrarPedido', views.administrarpedido, name="administrarpedido"),
    path('modificarPedido', views.modificarpedido, name="modificarpedido"),
    path('mostrarPedido', views.mostrarpedido, name="mostrarpedido"),
    path('historialPedidos', views.historialpedidos, name="historialpedidos"),
    path('ayudaempleado', views.ayudaempleado, name="ayudaempleado"),


]
