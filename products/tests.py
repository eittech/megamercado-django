from django.test import TestCase
from products.models import *
from products.forms import *

# Create your tests here.

class ShopGroupTestCase(TestCase):
    ''' Pruebas para la tabla de ShopGroup '''

    def setUp(self):
        pass

    '''Caso de prueba para verificar que se crea un shop group'''
    def test_shopgroup_crear(self):
        form_data = {
            'id_shop_group': "1",
            'name' : "Nombre grupo",
            'share_order': "True",
            'share_stock' : "False",
            'active': "True",
            'deleted': "False"
        }
        form = ShopGroupForm(data=form_data)
        form.save()
        group1 = ShopGroup.objects.get(name = "Nombre grupo")
        self.assertEqual(group1.name, "Nombre grupo")

    '''Caso de prueba para verificar que se elimina un shop group'''
    def test_shopgroup_eliminar(self):
        form_data = {
            'id_shop_group': "1",
            'name' : "Nombre grupo",
            'share_order': "True",
            'share_stock' : "False",
            'active': "True",
            'deleted': "False"
        }
        form = ShopGroupForm(data = form_data)
        form.save()
        group1 = ShopGroup.objects.get(name = "Nombre grupo").delete()
        try:
            group1 = ShopGroup.objects.get(name = "Nombre grupo")
        except:
            pass

    '''Caso de prueba para verificar que se edita un atributo de una tienda'''
    def test_shop_editar(self):
        form_data = {
            'id_shop' : "1",
            'name' : "Nombre"
        }
        form = ShopGroupForm(data=form_data)
        form.save()
        shop1 = ShopGroup.objects.get(name = "Nombre")
        shop1.name="Change"
        shop1.save()
        shop1 = ShopGroup.objects.get(name = "Change")
        self.assertEqual(shop1.name, "Change")

    ''' Caso de prueba para verificar si se añaden instancias que poseen strings vacios en
        el nombre del group shop. '''
    def test_shopgroup_sin_name(self):
        form_data = {
            'id_shop_group': "1",
            'name' : "",
            'share_order': "True",
            'share_stock' : "False",
            'active': "True",
            'deleted': "False"
        }
        form = ShopGroupForm(data=form_data)
        self.assertFalse(form.is_valid())

    ''' Caso de prueba para verificar si se añaden instancias que con solo el nombre del
        group shop. '''
    def test_shopgroup_solo_name(self):
        form_data = {
            'id_shop_group': "1",
            'name' : "Nombre grupo"
        }
        form = ShopGroupForm(data=form_data)
        form.save()
        group1 = ShopGroup.objects.get(name = "Nombre grupo")
        self.assertEqual(group1.name, "Nombre grupo")

    ''' Caso de prueba para verificar si se añaden instancias con estado activo y eliminado
        al mismo tiempo. '''
    def test_shopgroup_activo_y_eliminado(self):
        form_data = {
            'id_shop_group': "1",
            'name' : "Nombre",
            'share_order': "True",
            'share_stock' : "False",
            'active': "True",
            'deleted': "True"
        }
        form = ShopGroupForm(data=form_data)
        try:
            form.save
        except:
            pass

    ''' Caso de prueba para verificar si se añaden instancias sin el atributo booleano
        share_order del group shop. '''
    def test_shopgroup_sin_share_order(self):
        form_data = {
            'id_shop_group': "1",
            'name' : "Nombre",
            'share_stock' : "False",
            'active': "True",
            'deleted': "False"
        }
        form = ShopGroupForm(data=form_data)
        form.save()
        group1 = ShopGroup.objects.get(name = "Nombre")
        self.assertEqual(group1.name, "Nombre")

    ''' Caso de prueba para verificar si se añaden instancias sin el atributo booleano
        share_stock del group shop. '''
    def test_shopgroup_sin_share_stock(self):
        form_data = {
            'id_shop_group': "1",
            'name' : "Nombre",
            'share_order': "True",
            'active': "True",
            'deleted': "False"
        }
        form = ShopGroupForm(data=form_data)
        form.save()
        group1 = ShopGroup.objects.get(name = "Nombre")
        self.assertEqual(group1.name, "Nombre")
    
        ''' Caso de prueba para verificar si se añaden instancias sin el atributo booleano
        active del group shop. '''
    def test_shopgroup_sin_active(self):
        form_data = {
            'id_shop_group': "1",
            'name' : "Nombre",
            'share_order': "True",
            'share_stock' : "False",
            'deleted': "False"
        }
        form = ShopGroupForm(data=form_data)
        form.save()
        group1 = ShopGroup.objects.get(name = "Nombre")
        self.assertEqual(group1.name, "Nombre")

    ''' Caso de prueba para verificar si se añaden instancias sin el atributo booleano
        deleted del group shop. '''
    def test_shopgroup_sin_deleted(self):
        form_data = {
            'id_shop_group': "1",
            'name' : "Nombre",
            'share_order': "True",
            'share_stock' : "True",
            'active': "True"
        }
        form = ShopGroupForm(data=form_data)
        form.save()
        group1 = ShopGroup.objects.get(name = "Nombre")
        self.assertEqual(group1.name, "Nombre")
    
        ''' Caso de prueba para verificar si se añaden instancias sin el identificador
            del group shop. '''
    def test_shopgroup_sin_id(self):
        form_data = {
            'name' : "Nombre"
        }
        form = ShopGroupForm(data=form_data)
        form.save()
        group1 = ShopGroup.objects.get(name = "Nombre")
        self.assertEqual(group1.name, "Nombre")

class ShopTestCase(TestCase):
    ''' Pruebas para la tabla de ShopGroup '''

    def setUp(self):
        self.shopgroup = ShopGroup.objects.create(
            id_shop_group="1",
            name="Nombre grupo",
            share_order= "True",
            share_stock= "False",
            active= "True",
            deleted= "False")

    '''Caso de prueba para verificar que se crea una tienda'''
    def test_shop_crear(self):
        form_data = {
            'id_shop' : "1",
            'id_shop_group': self.shopgroup.id_shop_group,
            'name' : "Nombre",
            'active': "True",
            'deleted': "False",
            'virtual_url' : "www.google.com"
        }
        form = ShopForm(data=form_data)
        form.save()
        shop1 = Shop.objects.get(name = "Nombre")
        self.assertEqual(shop1.name, "Nombre")
    
    '''Caso de prueba para verificar que se crea una tienda'''
    def test_shop_eliminar(self):
        form_data = {
            'id_shop' : "1",
            'id_shop_group': self.shopgroup.id_shop_group,
            'name' : "Nombre",
            'active': "True",
            'deleted': "False",
            'virtual_url' : "www.google.com"
        }
        form = ShopForm(data=form_data)
        form.save()
        shop1 = Shop.objects.get(name = "Nombre").delete()
        try:
            shop1 = Shop.objects.get(name = "Nombre")
        except:
            pass

    '''Caso de prueba para verificar que se edita un atributo de una tienda'''
    def test_shop_editar(self):
        form_data = {
            'id_shop' : "1",
            'id_shop_group': self.shopgroup.id_shop_group,
            'name' : "Nombre"
        }
        form = ShopForm(data=form_data)
        form.save()
        shop1 = Shop.objects.get(name = "Nombre")
        shop1.name="Change"
        shop1.save()
        shop1 = Shop.objects.get(name = "Change")
        self.assertEqual(shop1.name, "Change")

    '''Caso de prueba para verificar que se crea una tienda solo con el nombre
        y la foranea al grupo de la tienda'''
    def test_shop_solo_name(self):
        form_data = {
            'id_shop' : "1",
            'id_shop_group': self.shopgroup.id_shop_group,
            'name' : "Nombre"
        }
        form = ShopForm(data=form_data)
        form.save()
        shop1 = Shop.objects.get(name = "Nombre")
        self.assertEqual(shop1.name, "Nombre")


    ''' Caso de prueba para verificar si se añaden instancias con estado activo y eliminado
        al mismo tiempo. '''
    def test_shop_activo_eliminado(self):
        form_data = {
            'id_shop' : "1",
            'id_shop_group': self.shopgroup.id_shop_group,
            'name' : "Nombre",
            'active': "True",
            'deleted': "True"
        }
        form = ShopForm(data=form_data)
        try:
            form.save()
        except:
            pass
    
    '''Caso de prueba para verificar si se crea una tienda con url malo'''
    def test_shop_url_malo(self):
        form_data = {
            'id_shop' : "1",
            'id_shop_group': self.shopgroup.id_shop_group,
            'name' : "Nombre",
            'virtual_url' : "www.googlecom"
        }
        form = ShopForm(data=form_data)
        try:
            form.save()
        except:
            pass
    
    '''Caso de prueba para verificar si se crea una tienda sin foranea'''
    def test_shop_sin_foranea(self):
        form_data = {
            'id_shop' : "1",
            'name' : "Nombre"
        }
        form = ShopForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    
    '''Caso de prueba para verificar si se crea una tienda con foranea mala'''
    def test_shop_foranea_mala(self):
        form_data = {
            'id_shop' : "1",
            'id_shop_group': "mala",
            'name' : "Nombre"
        }
        form = ShopForm(data=form_data)
        self.assertFalse(form.is_valid())

class AttributeGroupTestCase(TestCase):
    ''' Pruebas para la tabla de AttributeGroup '''

    def setUp(self):
        pass

    '''Caso de prueba para verificar que se crea un grupo de atributo'''
    def test_attributegroup_crear(self):
        form_data = {
            'id_attribute_group' : "1",
            'is_color_group': "True",
            'name' : "Nombre",
            'public_name': "Public name",
            'group_type': "Tipo",
            'position' : 1
        }
        form = AttributeGroupForm(data=form_data)
        form.save()
        ag1 = AttributeGroup.objects.get(name = "Nombre")
        self.assertEqual(ag1.name, "Nombre")
    
    '''Caso de prueba para verificar que se crea un grupo de atributo'''
    def test_attributegroup_eliminar(self):
        form_data = {
            'id_attribute_group' : "1",
            'is_color_group': "True",
            'name' : "Nombre",
            'public_name': "Public name",
            'group_type': "Tipo",
            'position' : 1
        }
        form = AttributeGroupForm(data=form_data)
        form.save()
        ag1 = AttributeGroup.objects.get(name = "Nombre").delete()
        try:
            ag1 = AttributeGroup.objects.get(name = "Nombre")
        except:
            pass

    '''Caso de prueba para verificar que se edita un atributo de un grupo de atributo'''
    def test_attributegroup_editar(self):
        form_data = {
            'id_attribute_group' : "1",
            'is_color_group': "True",
            'name' : "Nombre",
            'public_name': "Public name",
            'group_type': "Tipo",
            'position' : 1
        }
        form = AttributeGroupForm(data=form_data)
        form.save()
        ag1 = AttributeGroup.objects.get(name = "Nombre")
        ag1.name="Change"
        ag1.save()
        ag1 = AttributeGroup.objects.get(name = "Change")
        self.assertEqual(ag1.name, "Change")

    
    '''Caso de prueba para verificar si se crea un grupo de atributo
        con string vacio en name'''
    def test_attributegroup_sin_name(self):
        form_data = {
            'id_attribute_group' : "1",
            'is_color_group': "True",
            'name' : "",
            'public_name': "Public name",
            'group_type': "Tipo",
            'position' : 1
        }
        form = AttributeGroupForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    '''Caso de prueba para verificar si se crea un grupo de atributo
        con string vacio en public_name'''
    def test_attributegroup_sin_publicname(self):
        form_data = {
            'id_attribute_group' : "1",
            'is_color_group': "True",
            'name' : "Name",
            'public_name': "",
            'group_type': "Tipo",
            'position' : 1
        }
        form = AttributeGroupForm(data=form_data)
        self.assertFalse(form.is_valid())

    '''Caso de prueba para verificar si se crea un grupo de atributo
        con string vacio en group_type'''
    def test_attributegroup_sin_grouptype(self):
        form_data = {
            'id_attribute_group' : "1",
            'is_color_group': "True",
            'name' : "Name",
            'public_name': "Public name",
            'group_type': "",
            'position' : 1
        }
        form = AttributeGroupForm(data=form_data)
        self.assertFalse(form.is_valid())

    '''Caso de prueba para verificar si se crea un grupo de atributo
        con string en position'''
    def test_attributegroup_position_mal(self):
        form_data = {
            'id_attribute_group' : "1",
            'is_color_group': "True",
            'name' : "Nombre",
            'public_name': "Public name",
            'group_type': "Tipo",
            'position' : "hola"
        }
        form = AttributeGroupForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    '''Caso de prueba para verificar si se crea un grupo de atributo
        con numero negativo en position'''
    def test_attributegroup_position_negativo(self):
        form_data = {
            'id_attribute_group' : "1",
            'is_color_group': "True",
            'name' : "Nombre",
            'public_name': "Public name",
            'group_type': "Tipo",
            'position' : -1
        }
        form = AttributeGroupForm(data=form_data)
        self.assertFalse(form.is_valid())

class AttributeTestCase(TestCase):
    ''' Pruebas para la tabla de Attribute '''

    def setUp(self):
        self.attributegroup= AttributeGroup.objects.create(
            id_attribute_group="1",
            is_color_group="True",
            name="Nombre",
            public_name= "Public name",
            group_type= "Tipo",
            position= 1)


    '''Caso de prueba para verificar que se crea un atributo'''
    def test_attribute_crear(self):
        form_data = {
            'id_attribute' : "1", 
            'id_attribute_group' : self.attributegroup.id_attribute_group,
            'name' : "Nombre",
            'color': "Public name",
            'position' : 1
        }
        form = AttributeForm(data=form_data)
        form.save()
        ag1 = Attribute.objects.get(name = "Nombre")
        self.assertEqual(ag1.name, "Nombre")
    
    '''Caso de prueba para verificar que se crea un atributo'''
    def test_attribute_eliminar(self):
        form_data = {
            'id_attribute' : "1", 
            'id_attribute_group' : self.attributegroup.id_attribute_group,
            'name' : "Nombre",
            'color': "Public name",
            'position' : 1
        }
        form = AttributeForm(data=form_data)
        form.save()
        ag1 = Attribute.objects.get(name = "Nombre").delete()
        try:
            ag1 = Attribute.objects.get(name = "Nombre")
        except:
            pass

    '''Caso de prueba para verificar que se edita un atributo de un grupo de atributo'''
    def test_attribute_editar(self):
        form_data = {
            'id_attribute' : "1", 
            'id_attribute_group' : self.attributegroup.id_attribute_group,
            'name' : "Nombre",
            'color': "Public name",
            'position' : 1
        }
        form = AttributeForm(data=form_data)
        form.save()
        ag1 = Attribute.objects.get(name = "Nombre")
        ag1.name="Change"
        ag1.save()
        ag1 = Attribute.objects.get(name = "Change")
        self.assertEqual(ag1.name, "Change")

    '''Caso de prueba para verificar si se crea un grupo de atributo
        con string vacio en name'''
    def test_attribute_sin_name(self):
        form_data = {
            'id_attribute' : "1", 
            'id_attribute_group' : self.attributegroup.id_attribute_group,
            'name' : "",
            'color': "Public name",
            'position' : 1
        }
        form = AttributeForm(data=form_data)
        self.assertFalse(form.is_valid())

    '''Caso de prueba para verificar si se crea un atributo sin foranea'''
    def test_attribute_sin_foranea(self):
        form_data = {
            'id_attribute' : "1", 
            'name' : "Nombre",
            'color': "Public name",
            'position' : 1
        }
        form = AttributeForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    
    '''Caso de prueba para verificar si se crea un atributo con foranea mala'''
    def test_attribute_foranea_mala(self):
        form_data = {
            'id_attribute' : "1", 
            'id_attribute_group' : "mala",
            'name' : "Nombre",
            'color': "Public name",
            'position' : 1
        }
        form = AttributeForm(data=form_data)
        self.assertFalse(form.is_valid())

    '''Caso de prueba para verificar si se crea un atributo
        con string en position'''
    def test_attribute_position_mal(self):
        form_data = {
            'id_attribute' : "1", 
            'id_attribute_group' : self.attributegroup.id_attribute_group,
            'name' : "Nombre",
            'color': "Public name",
            'position' : "hola"
        }
        form = AttributeForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    '''Caso de prueba para verificar si se crea un atributo
        con numero negativo en position'''
    def test_attribute_position_negativo(self):
        form_data = {
            'id_attribute' : "1", 
            'id_attribute_group' : self.attributegroup.id_attribute_group,
            'name' : "Nombre",
            'color': "Public name",
            'position' : -1
        }
        form = AttributeForm(data=form_data)
        self.assertFalse(form.is_valid())