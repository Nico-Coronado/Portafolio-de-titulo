from django.db import models


class Detallepedido(models.Model):
    cantidadp = models.IntegerField()
    precio_pedido = models.IntegerField()
    producto_codigo_producto = models.IntegerField()
    orden_pedido_id = models.ForeignKey('OrdenPedido',models.DO_NOTHING,db_column='orden_pedido_id')

class OrdenPedido(models.Model):
    fecha_codp = models.DateTimeField(auto_now_add=True)
    estado_odp = models.IntegerField()
    precio_total_odp = models.IntegerField()
    fecha_rodp = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    empleado_rut_emp = models.CharField(max_length=20)
    proveedor_rut_prov = models.CharField(max_length=20)

