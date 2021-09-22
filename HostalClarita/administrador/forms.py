from django import forms
from django.forms.models import ModelForm
from .models import Plato, Habitacion,Comedor, FamiliaProducto, Moneda
from django.db import connection


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

    
class platoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super(platoForm, self).__init__(*args, **kwargs)
        self.fields['nombre_plato'].required = True      
        self.fields['dia_plato'].required = True      
        self.fields['hora_plato'].required = True      
        self.fields['precio_plato'].required = True      
        self.fields['comedor_id_comedor'].required = True      
        self.fields['comedor_id_comedor'].label = "Comedor"

    comedores=listarComedorCliente()
    #Se reemplaza el comedor_id_comedor por defecto.
    comedor_id_comedor = forms.ChoiceField(choices=comedores)
    

class habitacionForm(forms.ModelForm):

    class Meta:
        model = Habitacion
        fields = '__all__'


class comedorForm(forms.ModelForm):

    class Meta:
        model = Comedor
        fields= '__all__'
    def __init__(self, *args, **kwargs):
        super(comedorForm, self).__init__(*args, **kwargs)
        self.fields['servicio_comedor'].required = True


class comedorLeerform(forms.Form):
    idcomedor = forms.IntegerField(label='id comedor')

class comedorActuForm(forms.Form):
    idcomedora = forms.IntegerField(label='id comedor')
    nomCom = forms.CharField(label='Nombre Comedor', max_length=100)

class comedorEliForm(forms.Form):
    idcomedore = forms.IntegerField(label='id comedor')


class familiaProductoForm(forms.ModelForm):
    class Meta: 
        model = FamiliaProducto
        fields= '__all__'
    def __init__(self, *args, **kwargs):
        super(familiaProductoForm, self).__init__(*args, **kwargs)
        self.fields['nombre_familiap'].required = True      
        self.fields['nombre_familiap'].label = "Nombre Familia Producto"      


class famipEliForm(forms.Form):
    ide = forms.IntegerField(label='id familia producto')

class famipLeerForm(forms.Form):
    idl = forms.IntegerField(label='id familia producto')

class famipActuForm(forms.Form):
    ida = forms.IntegerField(label='id familia producto')
    nombre_familiap = forms.CharField(label='Nombre familia producto')

class moneForm(forms.ModelForm):
    class Meta:
        model = Moneda
        fields= '__all__'
    def __init__(self, *args, **kwargs):
        super(moneForm, self).__init__(*args, **kwargs)
        self.fields['codigo_moneda'].required = True      
        self.fields['valor_peso'].required = True      

class monLeerForm(forms.Form):
    idl = forms.IntegerField(label='Id Moneda')
    

class monActuForm(forms.Form):
    ida = forms.IntegerField(label='Id Moneda')
    codigo_moneda=forms.CharField(label='Codigo Moneda')
    valor_pesoa=forms.IntegerField(label='Valor Peso')


class monEliForm(forms.Form):
    ide= forms.IntegerField(label='id Moneda')