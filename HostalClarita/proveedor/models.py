from django.db import models
from administrador.models import FamiliaProducto

class Producto(models.Model):
  codigo_producto = models.IntegerField(blank=True, null=True)
  nombre_del_producto = models.CharField(max_length=50)
  marca_del_producto = models.CharField(max_length=50)
  descripcion_del_producto = models.CharField(max_length=1500)
  fecha_de_vencimiento = models.DateField()
  precio = models.IntegerField()
  stock = models.IntegerField()
  stock_critico = models.IntegerField()
  id_proveedor = models.IntegerField(blank=True, null=True)
  familia_producto = models.ForeignKey(FamiliaProducto, models.DO_NOTHING, db_column='familia_producto',blank=True, null=True)



