# Este modulo de django te dejara crear los formularios
# con 3 campos listos que son: username, password y la confirmacion del password
from django.contrib.auth.forms import UserCreationForm
# El modulo transaction guardara los cambios si el bloque de
# codigo corre perfectamente, sino es asi, hara un roolback
from django.db import transaction
from .models import Cliente, Empleado, Proveedor, User
from django import forms

class ClienteSignUpForm(UserCreationForm):
    rut = forms.CharField(required=True)
    nombre_empresa = forms.CharField(required = True)
    direccion = forms.CharField(required=True)
    telefono = forms.CharField(required=True)
    rut_representante = forms.CharField(required=True)
    nombre_representante = forms.CharField(required=True)
    cargo_empresa = forms.CharField(required = True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_cliente = True
        user.save()
        cliente = Cliente.objects.create(user=user)
        cliente.rut=self.cleaned_data.get('rut')
        cliente.nombre_empresa=self.cleaned_data.get('nombre_empresa')
        cliente.direccion=self.cleaned_data.get('direccion')
        cliente.telefono=self.cleaned_data.get('telefono')
        cliente.rutRepresentante=self.cleaned_data.get('rut_representante')
        cliente.nombre_representante=self.cleaned_data.get('nombre_representante')
        cliente.cargo_empresa=self.cleaned_data.get('cargo_empresa')

        cliente.save()
        return user


class EmpleadoSignUpForm(UserCreationForm):
    nombre_completo_empleado = forms.CharField(required =True)
    rut = forms.CharField(required = True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_empleado = True
        user.save()
        empleado = Empleado.objects.create(user=user)
        empleado.nombre_completo_empleado = self.cleaned_data.get('nombre_completo_empleado')
        empleado.rut = self.cleaned_data.get('rut')
        empleado.save()
        return user

class ProveedorSignUpForm(UserCreationForm):
    nombre_proveedor = forms.CharField(required = True)
    rubro = forms.CharField(required = True)
    numero_contacto = forms.CharField(required= True)
    rut = forms.CharField(required=True)
    direccion = forms.CharField(required = True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_proveedor = True
        user.save()
        proveedor = Proveedor.objects.create(user=user)
        proveedor.rut =self.cleaned_data.get('rut')
        proveedor.nombre_proveedor = self.cleaned_data.get('nombre_proveedor')
        proveedor.rubro = self.cleaned_data.get('rubro')
        proveedor.numero_contacto = self.cleaned_data.get('numero_contacto')
        proveedor.direccion = self.cleaned_data.get('direccion')
        proveedor.save()
        return user
