from django import forms
from .models import Producto

class productoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ['nombre_del_producto', 'marca_del_producto','descripcion_del_producto',
                'fecha_de_vencimiento','precio','stock','stock_critico','familia_producto']
        widgets = {
            'fecha_de_vencimiento': forms.DateInput(attrs={'type': 'date'})
            }
    def __init__(self, *args, **kwargs):
        super(productoForm, self).__init__(*args, **kwargs)
        self.fields['familia_producto'].required = True
