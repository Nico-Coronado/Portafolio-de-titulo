from django.urls import path
from .import views

urlpatterns = [
    path('', views.proveedor, name="proveedor"),
    path('producto/', views.crearproducto, name="crearproducto"),
    path('producto/borrar/<int:pk>/', views.producto_borrar, name="producto-borrar"),
    path('producto/actualizar/<int:pk>/', views.producto_actualizar, name="producto-actualizar"),

    path('ordenes-pendientes/', views.proveedor_lista, name="proveedor-lista"),
    path('mostrarPedidoProveedor', views.mostrarpedidop, name="mostrarpedidop"),
    path('historialPedidosp', views.historialpedidosp, name="historialpedidosp"),
    path('ayudaproveedor', views.ayudaproveedor, name="ayudaproveedor")



]
