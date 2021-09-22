from django.urls import path
from .import views


urlpatterns = [
    path('', views.portadacliente, name="portadacliente"),
    path('habitacion/', views.cliente, name="cliente-habitacion"),
    path('habitacion/lista-habitacion/', views.lista_habitacion, name="lista-habitacion"),
    path('confirmar-compra/', views.confirmar_compra, name="confirmar-compra"),
    path('habitacion/lista-habitacion/<int:pk>/agregar-huesped/', views.huesped, name="huesped"),
    path('habitacion/eliminar-huesped/<int:pk>/', views.eliminar_huesped, name="eliminar-huesped"),
    path('comedor/', views.comedor, name="cliente-comedor"),
    path('mis-compras/', views.misCompras, name="cliente-compras"),
    path('mis-compras/<int:pk>/', views.compra_detalle, name="compra-detalle"),
    path('habitacion-por-planilla/', views.habitacion_planilla, name="habitacion-planilla"),
    path('descargar-excel/', views.descargar_excel, name="descargar-excel"),
    path('factura/', views.factura, name="factura"),    
    path('actualizarMoneda/', views.actualizarMoneda, name="actualizar-moneda"),
    path('factura/descargar-pdf', views.export_pdf_factura, name="pdf-factura"),
    path('descargar-pdf/<int:pk>', views.export_pdf_mis_compras, name="pdf-factura-compras"),
    path('ayudacliente', views.ayudacliente, name="ayudacliente"),
    path('infohabitaciones', views.infohabitaciones, name="infohabitaciones"),
    path('infocomedores', views.infocomedores, name="infocomedores"),


    
]



