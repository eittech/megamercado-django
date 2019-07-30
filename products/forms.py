from django import forms
from .models import *
from comparagrow import settings

class TiendaForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos shop groups
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = Shop
        fields = ['name', 'logo']

class PreguntaForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos shop groups
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = MensajeProduct
        fields = ['pregunta']

class RespuestaForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos shop groups
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = MensajeProduct
        fields = ['respuesta', 'pregunta']

class ProductosForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos productos
    '''
    available_date=forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = Product
        fields = ['id_category_default','id_shop_default','name','description','description_short','online_only','ean13','upc' ,'quantity', 'minimal_quantity', 'price','wholesale_price','reference','width','height','depth', 'weight','out_of_stock','combination','active','available_date','condition','is_virtual']

class FotosForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos imagenes de los productos
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = Image
        fields = ['image','legend','position','cover']

class GrupoAttrShopForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos carrier shop
    '''
    id_attribute_group = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),queryset=AttributeGroup.objects.all())
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = AttributeGroupShop
        fields=['id_attribute_group']

class AttrForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos atributos
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = Attribute
        fields= ['name','color']

class CombAttrForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos carrier shop
    '''
    id = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),queryset=AttributeShop.objects.all())
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = AttributeShop
        fields=['id']
    
class CombForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos carrier shop
    '''
    image=forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),queryset=Image.objects.all())
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = ProductAttribute
        fields=['reference','ean13','upc','wholesale_price','quantity','weight','unit_price_impact','default_on','minimal_quantity','available_date']

class ViForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos shop groups
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = Product
        fields = ['visibility']

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

class GroupsForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos Groups
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = Groups
        fields = '__all__'

class CategoryGroupForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos CategoryGroup
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = CategoryGroup
        fields = '__all__'

class ProductForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos Product
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = Product
        fields = '__all__'

class CategoryProductForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos Category Product 
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = CategoryProduct
        fields = '__all__'

class ProductAttributeForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos Product Attribute
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = ProductAttribute
        fields = '__all__'

class ImageForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos Image
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = Image
        fields = '__all__'

class ProductAttributeCombinationForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos Product Attribute Combination
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = ProductAttributeCombination
        fields = '__all__'

class ProductAttributeImageForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos Product Attribute Image
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = ProductAttributeImage
        fields = '__all__'

class ProductAttributeShopForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos Product Attribute Shop
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = ProductAttributeShop
        fields = '__all__'

class ProductShopForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos Product Shop
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = ProductShop
        fields = '__all__'
    
class AttributeImpactForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos Attribute Impact
    '''
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = AttributeImpact
        fields = '__all__'