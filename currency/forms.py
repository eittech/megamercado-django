from django import forms
from .models import *


class CurrencyShopForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos CurrencyShop
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = CurrencyShop
        fields = ['id_currency', 'rate_moneda', 'rate_referencia']

class AccountForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos Account
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = Account
        fields = ['name', 'tipo', 'number', 'persona']