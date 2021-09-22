from django.db import models

# Create your models here.
# Definiendo los datos que se requieren para el registro de usuarios
class Visita(models.Model):
    ipvisita =  models.CharField(max_length=150)
    fechavisita = models.DateTimeField(auto_now_add=True)