from django import forms
from .models import *


class ZoneForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos Zone
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = Zone
        fields = '__all__'

class CountryForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos Country
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = Country
        fields = '__all__'

class CountryShopForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos CountryShop
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = CountryShop
        fields = '__all__'

class StateForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos State
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = State
        fields = '__all__'

class AddressForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos Address
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = Address
        fields = '__all__'

class DireccionForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos Address
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = Address
        fields = ['address1','address2','postcode','id_country','id_state','city','company','firstname','lastname','phone', 'phone_mobile', 'predeterminado']
