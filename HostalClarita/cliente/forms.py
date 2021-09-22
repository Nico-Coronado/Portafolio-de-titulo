from django import forms
from django.db import models,connection
from django.forms import fields
from .models import Huesped
from administrador.models import Comedor
import datetime
from django.core.exceptions import ValidationError


class huespedFechaForm(forms.ModelForm):

    class Meta:
        model = Huesped
        fields = ['fecha_de_inicio','fecha_de_termino']
        widgets = {
            'fecha_de_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_de_termino': forms.DateInput(attrs={'type': 'date'})
            }
    def __init__(self, *args, **kwargs):
        super(huespedFechaForm, self).__init__(*args, **kwargs)
        self.fields['fecha_de_inicio'].required = True
        self.fields['fecha_de_termino'].required = True
    def clean(self):
        cleaned_data = super(huespedFechaForm, self).clean()
        fecha_de_inicio = self.cleaned_data['fecha_de_inicio']
        fecha_de_termino = self.cleaned_data['fecha_de_termino']
        #Validación máximo estadía.
        # if fecha_de_termino > datetime.date.today() + datetime.timedelta(weeks=52):
        #     raise forms.ValidationError({"fecha_de_termino": "Fecha invalida, no se puede superar el rango de un año."})
        if fecha_de_inicio < datetime.date.today() :
            raise forms.ValidationError({"fecha_de_inicio": "El día de inicio no puede ser menos al de hoy."})
        if fecha_de_inicio == fecha_de_termino :
            raise forms.ValidationError({"fecha_de_termino": "La fecha de termino no puede ser el mismo día."})
        return cleaned_data   
           


class huespedForm(forms.ModelForm):

    class Meta:
        model = Huesped
        fields = ['rut','nombre']


def listarComedorCliente():
    try:
        listaComedor = []

        with connection.cursor() as cursorConsulta:
        #    print(cursorConsulta)
            cursorSalida = cursorConsulta.connection.cursor()
        #    print(cursorSalida)
            cursorConsulta.callproc('COMEDORPKG.listar_comedores', [cursorSalida])

        for comedor in cursorSalida:
            listaComedor.append(comedor)

        return listaComedor

    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        comedorErroneo = ['ERROR']
        return comedorErroneo



class minutaForm(forms.Form):
     comedores=listarComedorCliente()
     comedor = forms.ChoiceField(choices=comedores)
 


def listaMonedas():
    listaMonedas = []

    with connection.cursor() as cursorConsulta:
    #    print(cursorConsulta)
        cursorSalida = cursorConsulta.connection.cursor()
    #    print(cursorSalida)
        cursorConsulta.callproc('MONEDAPKG.listar_monedas', [cursorSalida])

    for moneda in cursorSalida:
        listaMonedas.append(moneda)

    return listaMonedas

class monedaForm(forms.Form):
     monedas=listaMonedas()
    # comedores = ['hola']
     moneda = forms.ChoiceField(choices=monedas)