from django import forms
from .models import *


class ShopGroupForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos shop groups
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = ShopGroup
        fields = '__all__'

class ShopForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos shop 
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = Shop
        fields = '__all__'

class AttributeGroupForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos Attribute Group 
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = AttributeGroup
        fields = '__all__'

class AttributeForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos Attribute
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = Attribute
        fields = '__all__'

class AttributeGroupShopForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos Attribute Group Shop
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = AttributeGroupShop
        fields = '__all__'

class AttributeShopForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos Attribute Shop
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = AttributeShop
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos Category
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = Category
        fields = '__all__'