from django import forms
from .models import *

class EnvioForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos transaciones
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = Orders
        fields = ['shipping_number', 'shipping_date', 'delivery_date']

class TransForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos transaciones
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = Transaction
        fields = ['id_acount','tipo','amount','description','observation', 'date_add']

class cartProForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos shop groups
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = CartProduct
        fields = ['id_product','quantity']