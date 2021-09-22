from django.db import models

# comedor
opcion_plato = [
    [1, "Lunes"],
    [2, "Martes"],
    [3, "Miercoles"],
    [4, "Jueves"],
    [5, "Viernes"],
    [6, "Sabado"],
    [7, "Domingo"]
]

Servicio = [ 
    [0, "General"],
    [1, "Ejecutivo"],
    [2, "Premium"]
]

class Comedor(models.Model):
    servicio_comedor = models.CharField(max_length=200,blank=True, null=True)

    def __str__(self):
        return self.servicio_comedor

dias = [
    ['','Seleccione el dia'],
    [1,'Lunes'],
    [2,'Martes'],
    [3,'Miercoles'],
    [4,'Jueves'],
    [5,'Viernes'],
    [6,'Sabado'],
    [7,'Domingo'],
]

hora = [
    ['','Seleccione la hora'],
    ['10:00 AM','Desayuno'],
    ['14:00 PM','Almuerzo'],
    ['19:00 PM','Once'],
    
]

class Plato(models.Model):
    nombre_plato = models.CharField(max_length=200,blank=True, null=True)
    dia_plato = models.BigIntegerField(choices=dias ,blank=True, null=True)
    hora_plato = models.CharField(choices=hora,max_length=50,blank=True, null=True)
    precio_plato = models.BigIntegerField(blank=True, null=True)
    comedor_id_comedor = models.BigIntegerField()

    def __str__(self):
        return self.comedor_id_comedor

    

# Habitacion

disponibilidad = [
    [0, 'Disponible'],
    [1, 'No esta disponible por estar en mantenimiento'],
    [2, 'No esta disponible por estar asignado a la empresa']
]

class Habitacion(models.Model):
    numero_de_habitacion = models.IntegerField()
    descripcion_de_la_habitacion = models.CharField(max_length=1500)
    disponibilidad_habitacion = models.IntegerField(choices=disponibilidad)
    precio = models.IntegerField()

    def __str__(self) -> str:
        return super().__str__()

class FamiliaProducto(models.Model):
    nombre_familiap = models.CharField(max_length=100,blank=True, null=True)
    
    def __str__(self):
        return self.nombre_familiap

class Moneda(models.Model):
    codigo_moneda = models.CharField(max_length=100,blank=True,null=True)
    valor_peso = models.IntegerField(blank=True, null=True)
