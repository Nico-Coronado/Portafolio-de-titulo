from django.contrib import admin
from .models import User, Cliente, Proveedor, Empleado

admin.site.register(User)
admin.site.register(Cliente)
admin.site.register(Empleado)
admin.site.register(Proveedor)

