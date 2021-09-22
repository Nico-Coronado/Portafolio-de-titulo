from django.db import models

from django.contrib.auth.models import AbstractUser

# Creando los diferentes usuarios
class User(AbstractUser):
    is_empleado = models.BooleanField(default=False)
    is_proveedor = models.BooleanField(default=False)
    is_cliente = models.BooleanField(default=False)
# Definiendo los datos que se requieren para el registro de usuarios
class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    nombre_completo_empleado = models.CharField(max_length=50)
    rut = models.CharField(max_length=10)

class Proveedor(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    nombre_proveedor = models.CharField(max_length=50)
    rubro = models.CharField(max_length=100)
    numero_contacto = models.CharField(max_length=60, blank=True, null=True)
    rut = models.CharField(max_length=15,  blank=True, null=True)
    direccion = models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return self.nombre_proveedor

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    nombre_empresa = models.CharField(max_length=50)
    cargo_empresa = models.CharField(max_length=100)
    rut = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    rutRepresentante = models.CharField(max_length=15, blank=True, null=True)
    nombre_representante = models.CharField(max_length=100,blank=True, null=True)
