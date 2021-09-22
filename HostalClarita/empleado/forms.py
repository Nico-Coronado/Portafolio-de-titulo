from django import forms
from django.db import models,connection
from django.forms import fields
from account.models import Proveedor

class proveedoresForm(forms.Form):
    proveedores = forms.ModelChoiceField(queryset=Proveedor.objects.all().order_by('nombre_proveedor'))