from django.urls import path
from .import views

urlpatterns = [
    path('', views.portadaadmin, name='portadaadmin'),
    path('habitacion/', views.admin_habitacion, name='admin-habitacion'),

    path('habitacion/borrar/<str:pk>/', views.admin_habitacion_borrar, name='habitacion-borrar'),
    path('habitacion/actualizar/<str:pk>/', views.admin_habitacion_actualizar, name='habitacion-actualizar'),
    
    path('historial-huespedes/', views.admin_huesped, name='admin-huesped'),
    path('huespedes-actuales/', views.huespedesactuales, name='admin-huespedesa'),

    path('facturas/', views.admin_facturas, name='admin-facturas'),
    path('facturas/<int:pk>/', views.admin_facturas_borrar, name='facturas-borrar'),

    path('plato/', views.admin_plato, name='admin-plato'),
    path('comedor/', views.admin_comedor, name='admin-comedor'),
    path('pedidos/', views.admin_pedidos, name='admin-pedidos'),
    path('estadistica/', views.admin_estadistica, name='admin-estadistica'),

    path('plato/borrar/<int:pk>/', views.plato_eli, name='plato-eli'),
    path('plato/actualizar/<int:pk>/', views.plato_actu, name='plato-actu'),
    
    path('familia-producto/',views.productFam,name='admin-famip' ),
    path('moneda/',views.moneda,name='admin-moneda'),

    path('ayudaadministrador/',views.ayudaadministrador,name='ayudaadministrador'),
    path('listaproductos/',views.mostrarProductos,name='listaproductos'),
    path('sistemahostal/',views.sistemahostal,name='sistemahostal')



]
