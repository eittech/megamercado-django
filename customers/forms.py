from django import forms
from .models import Customer
from django.contrib.auth.forms import UserCreationForm


class ImageFileUploadForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('image',) 

class CustomUserCreationForm(UserCreationForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos usuarios del sistema
    '''
    class Meta(UserCreationForm.Meta):
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = Customer
        #fields = ( 'username','first_name','last_name', 'email','alias', 'dni_type', 'image','dni','gender','firts_date','tipo', 'rol')
        fields = ( 'username','first_name','last_name', 'email')

class MisDatosCreationForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos usuarios del sistema
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = Customer
        fields = ['alias','dni_type','dni', 'gender','firts_date', 'website']

class SolicitudVendedorCreationForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos usuarios del sistema
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = Customer
        fields = ('image',)
