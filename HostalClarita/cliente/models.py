from django.db import models
from django.db.models.fields import BooleanField, IntegerField
from account.models import Cliente

class Fecha(models.Model):
    fecha_de_inicio = models.CharField(max_length=15)
    fecha_de_termino = models.CharField(max_length=15)

class Huesped(models.Model):
    rut = models.CharField(max_length=12)
    nombre = models.CharField(max_length=50) 
    fecha_de_inicio = models.DateField(blank=True, null=True)
    fecha_de_termino = models.DateField(blank=True, null=True)
    orden_de_compra = models.IntegerField(blank=True, null=True)
    numero_de_habitacion = models.IntegerField(blank=True, null=True)
    precio = IntegerField(blank=True, null=True)
    estado_huesped = IntegerField(blank=True, null=True)

class OrdenDeCompra(models.Model):
    numero_oc = models.BigIntegerField(primary_key=True)
    fecha_oc = models.DateTimeField(auto_now_add=True)
    valor_oc = models.BigIntegerField()
    cliente_rut_empresa = models.CharField(max_length=20)

class Factura(models.Model):
    codigo_factura = models.BigIntegerField(primary_key=True)
    fecha_emision = models.DateField()
    valor_bruto = models.BigIntegerField()
    valor_neto = models.BigIntegerField()
    precio_total = models.BigIntegerField()
    orden_de_compra_numero_oc = models.ForeignKey('OrdenDeCompra', models.DO_NOTHING, db_column='orden_de_compra_numero_oc')
