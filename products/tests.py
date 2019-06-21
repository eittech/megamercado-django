from django.test import TestCase
from products.models import *
from products.forms import *
from datetime import datetime
from django.utils import timezone

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
    def test_shopgroup_editar(self):
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
    ''' Pruebas para la tabla de Shop '''

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

class AttributeGroupShopTestCase(TestCase):
    ''' Pruebas para la tabla de AttributeGroupShop '''

    def setUp(self):
        self.attributegroup= AttributeGroup.objects.create(
            id_attribute_group="1",
            is_color_group="True",
            name="Nombre",
            public_name= "Public name",
            group_type= "Tipo",
            position= 1)
        self.shopgroup = ShopGroup.objects.create(
            id_shop_group="2",
            name="Nombre grupo",
            share_order= "True",
            share_stock= "False",
            active= "True",
            deleted= "False")
        self.shop= Shop.objects.create(
            id_shop= "1",
            id_shop_group= self.shopgroup,
            name="Nombre"
        )


    '''Caso de prueba para verificar que se crea un atributo de un grupo de tienda'''
    def test_attributegroupshop_crear(self):
        form_data = {
            'id_attribute_group' : self.attributegroup.id_attribute_group,
            'id_shop' : self.shop.id_shop
        }
        form = AttributeGroupShopForm(data=form_data)
        form.save()
        ag1 = AttributeGroupShop.objects.get(id_shop = "1")
        self.assertEqual(ag1.id_shop.name, "Nombre")
    
    '''Caso de prueba para verificar que se crea un atributo de un grupo de tienda'''
    def test_attributegroupshop_eliminar(self):
        form_data = {
            'id_attribute_group' : self.attributegroup.id_attribute_group,
            'id_shop' : self.shop.id_shop
        }
        form = AttributeGroupShopForm(data=form_data)
        form.save()
        ag1 = AttributeGroupShop.objects.get(id_shop = "1").delete()
        try:
            ag1 = AttributeGroupShop.objects.get(id_shop = "1")
        except:
            pass
    
    '''Caso de prueba para verificar que se crea un atributo de un grupo 
        de tienda sin foranea'''
    def test_attributegroupshop_sin_foranea(self):
        form_data = {
            'id_shop' : self.shop.id_shop
        }
        form = AttributeGroupShopForm(data=form_data)
        self.assertFalse(form.is_valid())

    '''Caso de prueba para verificar si se crea un atributo de un grupo 
        de tienda con foranea mala'''
    def test_attributegroupshop_foranea_mala(self):
        form_data = {
            'id_attribute_group' : self.attributegroup.id_attribute_group,
            'id_shop' : "mala",
        }
        form = AttributeGroupShopForm(data=form_data)
        self.assertFalse(form.is_valid())

class AttributeShopTestCase(TestCase):
    ''' Pruebas para la tabla de AttributeShop '''

    def setUp(self):
        self.attributegroup= AttributeGroup.objects.create(
            id_attribute_group="1",
            is_color_group="True",
            name="Nombre",
            public_name= "Public name",
            group_type= "Tipo",
            position= 1)
        self.attribute =Attribute.objects.create(
            id_attribute="1", 
            id_attribute_group=self.attributegroup,
            name="Nombre",
            color= "Public name",
            position=1
        )
        self.shopgroup = ShopGroup.objects.create(
            id_shop_group="2",
            name="Nombre grupo",
            share_order= "True",
            share_stock= "False",
            active= "True",
            deleted= "False")
        self.shop= Shop.objects.create(
            id_shop= "1",
            id_shop_group= self.shopgroup,
            name="Nombre"
        )

    '''Caso de prueba para verificar que se crea un atributo de una tienda'''
    def test_attributeshop_crear(self):
        form_data = {
            'id_attribute' : self.attribute.id_attribute,
            'id_shop' : self.shop.id_shop
        }
        form = AttributeShopForm(data=form_data)
        form.save()
        ag1 = AttributeShop.objects.get(id_shop = "1")
        self.assertEqual(ag1.id_shop.name, "Nombre")
    
    '''Caso de prueba para verificar que se crea un atributo de una tienda'''
    def test_attributeshop_eliminar(self):
        form_data = {
            'id_attribute' : self.attribute.id_attribute,
            'id_shop' : self.shop.id_shop
        }
        form = AttributeShopForm(data=form_data)
        form.save()
        ag1 = AttributeShop.objects.get(id_shop = "1").delete()
        try:
            ag1 = AttributeShop.objects.get(id_shop = "1")
        except:
            pass

    '''Caso de prueba para verificar que se crea un atributo de una 
        tienda sin foranea'''
    def test_attributeshop_sin_foranea(self):
        form_data = {
            'id_shop' : self.shop.id_shop
        }
        form = AttributeShopForm(data=form_data)
        self.assertFalse(form.is_valid())

    '''Caso de prueba para verificar si se crea un atributo de una 
        tienda con foranea mala'''
    def test_attributeshop_foranea_mala(self):
        form_data = {
            'id_attribute' : self.attribute.id_attribute,
            'id_shop' : "mala",
        }
        form = AttributeShopForm(data=form_data)
        self.assertFalse(form.is_valid())

class CategoryTestCase(TestCase):
    ''' Pruebas para la tabla de Category '''

    def setUp(self):
        pass

    '''Caso de prueba para verificar que se crea unn Categoria'''
    def test_category_crear(self):
        form_data = {
            'id_category': "1",
            'name' : "Nombre",
            'description': "Description",
            'level_depth': 0,
            'active': "True",
            'date_add': "2018-07-29 09:17:13.812189",
            'date_upd': "2018-07-29 09:17:13.812189",
            'position': 1,
            'is_root_category': "False"
        }
        form = CategoryForm(data=form_data)
        form.save()
        group1 = Category.objects.get(name = "Nombre")
        self.assertEqual(group1.name, "Nombre")
    
    '''Caso de prueba para verificar que se elimina una Categoria'''
    def test_category_eliminar(self):
        form_data = {
            'id_category': "1",
            'name' : "Nombre",
            'description': "Description",
            'level_depth': 0,
            'active': "True",
            'date_add': "2018-07-29 09:17:13.812189",
            'date_upd': "2018-07-29 09:17:13.812189",
            'position': 1,
            'is_root_category': "False"
        }
        form = CategoryForm(data=form_data)
        form.save()
        group1 = Category.objects.get(name = "Nombre").delete()
        try:
            group1 = Category.objects.get(name = "Nombre")
        except:
            pass

    '''Caso de prueba para verificar que se edita una categoria'''
    def test_category_editar(self):
        form_data = {
            'id_category': "1",
            'name' : "Nombre",
            'description': "Description",
            'level_depth': 0,
            'active': "True",
            'date_add': "2018-07-29 09:17:13.812189",
            'date_upd': "2018-07-29 09:17:13.812189",
            'position': 1,
            'is_root_category': "False"
        }
        form = CategoryForm(data=form_data)
        form.save()
        shop1 = Category.objects.get(name = "Nombre")
        shop1.name="Change"
        shop1.save()
        shop1 = Category.objects.get(name = "Change")
        self.assertEqual(shop1.name, "Change")

    ''' Caso de prueba para verificar si se añaden instancias que poseen strings vacios en
        el nombre de la categoria. '''
    def test_category_sin_name(self):
        form_data = {
            'id_category': "1",
            'name' : "",
            'description': "Description",
            'level_depth': 0,
            'active': "True",
            'date_add': "2018-07-29 09:17:13.812189",
            'date_upd': "2018-07-29 09:17:13.812189",
            'position': 1,
            'is_root_category': "False"
        }
        form = CategoryForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    ''' Caso de prueba para verificar si se añaden instancias que poseen strings vacios en
        la fecha de la categoria. '''
    def test_category_sin_fecha(self):
        form_data = {
            'id_category': "1",
            'name' : "Name",
            'description': "Description",
            'level_depth': 0,
            'active': "True",
            'date_add': "",
            'date_upd': "2018-07-29 09:17:13.812189",
            'position': 1,
            'is_root_category': "False"
        }
        form = CategoryForm(data=form_data)
        self.assertFalse(form.is_valid())

    '''Caso de prueba para verificar si se crea una categoria
        con string en position'''
    def test_category_position_mal(self):
        form_data = {
            'id_category': "1",
            'name' : "Nombre",
            'description': "Description",
            'level_depth': 0,
            'active': "True",
            'date_add': "2018-07-29 09:17:13.812189",
            'date_upd': "2018-07-29 09:17:13.812189",
            'position': "hola",
            'is_root_category': "False"
        }
        form = CategoryForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    '''Caso de prueba para verificar si se crea una categoria
        con numero negativo en position'''
    def test_category_position_negativo(self):
        form_data = {
            'id_category': "1",
            'name' : "Nombre",
            'description': "Description",
            'level_depth': 0,
            'active': "True",
            'date_add': "2018-07-29 09:17:13.812189",
            'date_upd': "2018-07-29 09:17:13.812189",
            'position': -1,
            'is_root_category': "False"
        }
        form = CategoryForm(data=form_data)
        self.assertFalse(form.is_valid())

class GroupsTestCase(TestCase):
    ''' Pruebas para la tabla de Groups '''

    def setUp(self):
        pass

    '''Caso de prueba para verificar que se crea un grupo'''
    def test_groups_crear(self):
        form_data = {
            'id_group': "1",
            'name' : "Nombre",
            'reduction': 2,
            'price_display_method': 0,
            'show_prices': "True",
            'date_add': "2018-07-29 09:17:13.812189",
            'date_upd': "2018-07-29 09:17:13.812189"
        }
        form = GroupsForm(data=form_data)
        form.save()
        group1 = Groups.objects.get(name = "Nombre")
        self.assertEqual(group1.name, "Nombre")
    
    '''Caso de prueba para verificar que se elimina un grupo'''
    def test_groups_eliminar(self):
        form_data = {
            'id_group': "1",
            'name' : "Nombre",
            'reduction': 2,
            'price_display_method': 0,
            'show_prices': "True",
            'date_add': "2018-07-29 09:17:13.812189",
            'date_upd': "2018-07-29 09:17:13.812189"
        }
        form = GroupsForm(data=form_data)
        form.save()
        group1 = Groups.objects.get(name = "Nombre").delete()
        try:
            group1 = Groups.objects.get(name = "Nombre")
        except:
            pass

    '''Caso de prueba para verificar que se edita un grupo'''
    def test_groups_editar(self):
        form_data = {
            'id_group': "1",
            'name' : "Nombre",
            'reduction': 2,
            'price_display_method': 0,
            'show_prices': "True",
            'date_add': "2018-07-29 09:17:13.812189",
            'date_upd': "2018-07-29 09:17:13.812189"
        }
        form = GroupsForm(data=form_data)
        form.save()
        shop1 = Groups.objects.get(name = "Nombre")
        shop1.name="Change"
        shop1.save()
        shop1 = Groups.objects.get(name = "Change")
        self.assertEqual(shop1.name, "Change")

    ''' Caso de prueba para verificar si se añaden instancias que poseen strings vacios en
        el nombre del grupo. '''
    def test_cgroups_sin_name(self):
        form_data = {
            'id_group': "1",
            'name' : "",
            'reduction': 2,
            'price_display_method': 0,
            'show_prices': "True",
            'date_add': "2018-07-29 09:17:13.812189",
            'date_upd': "2018-07-29 09:17:13.812189"
        }
        form = CategoryForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    ''' Caso de prueba para verificar si se añaden instancias que poseen strings vacios en
        la fecha de un grupo. '''
    def test_groups_sin_fecha(self):
        form_data = {
            'id_group': "1",
            'name' : "Nombre",
            'reduction': 2,
            'price_display_method': 0,
            'show_prices': "True",
            'date_add': "",
            'date_upd': "2018-07-29 09:17:13.812189"
        }
        form = CategoryForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    ''' Caso de prueba para verificar si se añaden instancias que poseen mal el atributo
        reduction de un grupo. '''
    def test_groups_reduction_mal(self):
        form_data = {
            'id_group': "1",
            'name' : "Nombre",
            'reduction': "hola",
            'price_display_method': 0,
            'show_prices': "True",
            'date_add': "2018-07-29 09:17:13.812189",
            'date_upd': "2018-07-29 09:17:13.812189"
        }
        form = CategoryForm(data=form_data)
        self.assertFalse(form.is_valid())

class CategoryGroupTestCase(TestCase):
    ''' Pruebas para la tabla de CategoryGroup '''

    def setUp(self):
        self.groups= Groups.objects.create(
            id_group= "1",
            name= "Nombre",
            reduction= 2,
            price_display_method= 0,
            show_prices= "True",
            date_add=timezone.now(),
            date_upd= timezone.now()
        )
        self.categoria = Category.objects.create(
            id_category= "1",
            name="Nombre",
            description= "Description",
            level_depth= 0,
            active= "True",
            date_add= timezone.now(),
            date_upd= timezone.now(),
            position= 1,
            is_root_category= "False"
        )
    
    '''Caso de prueba para verificar que se crea una categoria de un grupo'''
    def test_categorygroup_crear(self):
        form_data = {
            'id_category' : self.categoria.id_category,
            'id_group' : self.groups.id_group
        }
        form = CategoryGroupForm(data=form_data)
        form.save()
        ag1 = CategoryGroup.objects.get(id_group = "1")
        self.assertEqual(ag1.id_group.name, "Nombre")
    
    '''Caso de prueba para verificar que se elimina una categoria de un grupo'''
    def test_categorygroup_eliminar(self):
        form_data = {
            'id_category' : self.categoria.id_category,
            'id_group' : self.groups.id_group
        }
        form = CategoryGroupForm(data=form_data)
        form.save()
        ag1 = CategoryGroup.objects.get(id_group = "1").delete()
        try:
            ag1 = CategoryGroup.objects.get(id_group = "1")
        except:
            pass

    '''Caso de prueba para verificar que se crea una categoria de un grupo
        sin foranea'''
    def test_categorygroup_sin_foranea(self):
        form_data = {
            'id_group' : self.groups.id_group
        }
        form = CategoryGroupForm(data=form_data)
        self.assertFalse(form.is_valid())

    '''Caso de prueba para verificar si se crea una categoria de un grupo
        con foranea mala'''
    def test_categorygroup_foranea_mala(self):
        form_data = {
            'id_category' : self.categoria.id_category,
            'id_group' : "mala"
        }
        form = CategoryGroupForm(data=form_data)
        self.assertFalse(form.is_valid())

class ProductTestCase(TestCase):
    ''' Pruebas para la tabla de Products '''

    def setUp(self):
        self.categoria = Category.objects.create(
            id_category= "1",
            name="Nombre",
            description= "Description",
            level_depth= 0,
            active= "True",
            date_add= timezone.now(),
            date_upd= timezone.now(),
            position= 1,
            is_root_category= "False"
        )
        self.shopgroup = ShopGroup.objects.create(
            id_shop_group="2",
            name="Nombre grupo",
            share_order= "True",
            share_stock= "False",
            active= "True",
            deleted= "False")
        self.shop= Shop.objects.create(
            id_shop= "1",
            id_shop_group= self.shopgroup,
            name="Nombre"
        )

    '''Caso de prueba para verificar que se crea un Producto'''
    def test_product_crear(self):
        form_data = {
            'id_product':"1",
            'id_category_default' : self.categoria.id_category,
            'id_shop_default': self.shop.id_shop,
            'name' : "Nombre",
            'on_sale' : "True",
            'online_only' : "True",
            'quantity' : 0,
            'minimal_quantity': 0,
            'price': 1,
            'wholesale_price': 0,
            'unit_price_ratio': 0,
            'additional_shipping_cost':1,
            'width':1,
            'height':1,
            'depth':1,
            'weight':1,
            'out_of_stock': 0,
            'available_for_order':"True",
            'available_date': "2018-07-29",
            'condition': "new",
            'visibility': "everywhere",
            'is_virtual':"True",
            'date_add': "2018-07-29 09:17:13.812189",
            'date_upd': "2018-07-29 09:17:13.812189"
        }
        form = ProductForm(data=form_data)
        form.save()
        group1 = Product.objects.get(name = "Nombre")
        self.assertEqual(group1.name, "Nombre")
    
    '''Caso de prueba para verificar que se elimina un Producto'''
    def test_product_eliminar(self):
        form_data = {
            'id_product':"1",
            'id_category_default' : self.categoria.id_category,
            'id_shop_default': self.shop.id_shop,
            'name' : "Nombre",
            'on_sale' : "True",
            'online_only' : "True",
            'quantity' : 0,
            'minimal_quantity': 0,
            'price': 1,
            'wholesale_price': 0,
            'unit_price_ratio': 0,
            'additional_shipping_cost':1,
            'width':1,
            'height':1,
            'depth':1,
            'weight':1,
            'out_of_stock': 0,
            'available_for_order':"True",
            'available_date': "2018-07-29",
            'condition': "new",
            'visibility': "everywhere",
            'is_virtual':"True",
            'date_add': "2018-07-29 09:17:13.812189",
            'date_upd': "2018-07-29 09:17:13.812189"
        }
        form = ProductForm(data=form_data)
        form.save()
        group1 = Product.objects.get(name = "Nombre").delete()
        try:
            group1 = Product.objects.get(name = "Nombre")
        except:
            pass

    '''Caso de prueba para verificar que se crea un Producto'''
    def test_product_editar(self):
        form_data = {
            'id_product':"1",
            'id_category_default' : self.categoria.id_category,
            'id_shop_default': self.shop.id_shop,
            'name' : "Nombre",
            'on_sale' : "True",
            'online_only' : "True",
            'quantity' : 0,
            'minimal_quantity': 0,
            'price': 1,
            'wholesale_price': 0,
            'unit_price_ratio': 0,
            'additional_shipping_cost':1,
            'width':1,
            'height':1,
            'depth':1,
            'weight':1,
            'out_of_stock': 0,
            'available_for_order':"True",
            'available_date': "2018-07-29",
            'condition': "new",
            'visibility': "everywhere",
            'is_virtual':"True",
            'date_add': "2018-07-29 09:17:13.812189",
            'date_upd': "2018-07-29 09:17:13.812189"
        }
        form = ProductForm(data=form_data)
        form.save()
        group1 = Product.objects.get(name = "Nombre")
        group1.name="Change"
        group1.save()
        group1 = Product.objects.get(name = "Change")
        self.assertEqual(group1.name, "Change")

    '''Caso de prueba para verificar si se crea un producto con
        string vacio en el nombre'''
    def test_product_sin_name(self):
        form_data = {
            'id_product':"1",
            'id_category_default' : self.categoria.id_category,
            'id_shop_default': self.shop.id_shop,
            'name' : "",
            'on_sale' : "True",
            'online_only' : "True",
            'quantity' : 0,
            'minimal_quantity': 0,
            'price': 1,
            'wholesale_price': 0,
            'unit_price_ratio': 0,
            'additional_shipping_cost':1,
            'width':1,
            'height':1,
            'depth':1,
            'weight':1,
            'out_of_stock': 0,
            'available_for_order':"True",
            'available_date': "2018-07-29",
            'condition': "new",
            'visibility': "everywhere",
            'is_virtual':"True",
            'date_add': "2018-07-29 09:17:13.812189",
            'date_upd': "2018-07-29 09:17:13.812189"
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())

    '''Caso de prueba para verificar si se crea un producto sin foranea'''
    def test_product_sin_foranea(self):
        form_data = {
            'id_product':"1",
            'id_shop_default': self.shop.id_shop,
            'name' : "Nombre",
            'on_sale' : "True",
            'online_only' : "True",
            'quantity' : 0,
            'minimal_quantity': 0,
            'price': 1,
            'wholesale_price': 0,
            'unit_price_ratio': 0,
            'additional_shipping_cost':1,
            'width':1,
            'height':1,
            'depth':1,
            'weight':1,
            'out_of_stock': 0,
            'available_for_order':"True",
            'available_date': "2018-07-29",
            'condition': "new",
            'visibility': "everywhere",
            'is_virtual':"True",
            'date_add': "2018-07-29 09:17:13.812189",
            'date_upd': "2018-07-29 09:17:13.812189"
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    
    '''Caso de prueba para verificar si se crea un producto con foranea mala'''
    def test_product_foranea_mala(self):
        form_data = {
            'id_product':"1",
            'id_category_default' : self.categoria.id_category,
            'id_shop_default': "mala",
            'name' : "Nombre",
            'on_sale' : "True",
            'online_only' : "True",
            'quantity' : 0,
            'minimal_quantity': 0,
            'price': 1,
            'wholesale_price': 0,
            'unit_price_ratio': 0,
            'additional_shipping_cost':1,
            'width':1,
            'height':1,
            'depth':1,
            'weight':1,
            'out_of_stock': 0,
            'available_for_order':"True",
            'available_date': "2018-07-29",
            'condition': "new",
            'visibility': "everywhere",
            'is_virtual':"True",
            'date_add': "2018-07-29 09:17:13.812189",
            'date_upd': "2018-07-29 09:17:13.812189"
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())

    '''Caso de prueba para verificar si se crea un producto con precio negativo'''
    def test_product_precio_negativo(self):
        form_data = {
            'id_product':"1",
            'id_category_default' : self.categoria.id_category,
            'id_shop_default': self.shop.id_shop,
            'name' : "Nombre",
            'on_sale' : "True",
            'online_only' : "True",
            'quantity' : 0,
            'minimal_quantity': 0,
            'price': -1,
            'wholesale_price': 0,
            'unit_price_ratio': 0,
            'additional_shipping_cost':1,
            'width':1,
            'height':1,
            'depth':1,
            'weight':1,
            'out_of_stock': 0,
            'available_for_order':"True",
            'available_date': "2018-07-29",
            'condition': "new",
            'visibility': "everywhere",
            'is_virtual':"True",
            'date_add': "2018-07-29 09:17:13.812189",
            'date_upd': "2018-07-29 09:17:13.812189"
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    '''Caso de prueba para verificar si se crea un producto sin fecha disponible'''
    def test_product_sin_fecha_disponible(self):
        form_data = {
            'id_product':"1",
            'id_category_default' : self.categoria.id_category,
            'id_shop_default': self.shop.id_shop,
            'name' : "Nombre",
            'on_sale' : "True",
            'online_only' : "True",
            'quantity' : 0,
            'minimal_quantity': 0,
            'price': 1,
            'wholesale_price': 0,
            'unit_price_ratio': 0,
            'additional_shipping_cost':1,
            'width':1,
            'height':1,
            'depth':1,
            'weight':1,
            'out_of_stock': 0,
            'available_for_order':"True",
            'available_date': "",
            'condition': "new",
            'visibility': "everywhere",
            'is_virtual':"True",
            'date_add': "2018-07-29 09:17:13.812189",
            'date_upd': "2018-07-29 09:17:13.812189"
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())

class CategoryProductTestCase(TestCase):
    ''' Pruebas para la tabla de CategoryProduct '''

    def setUp(self):
        self.categoria = Category.objects.create(
            id_category= "1",
            name="Nombre",
            description= "Description",
            level_depth= 0,
            active= "True",
            date_add= timezone.now(),
            date_upd= timezone.now(),
            position= 1,
            is_root_category= "False"
        )
        self.shopgroup = ShopGroup.objects.create(
            id_shop_group="2",
            name="Nombre grupo",
            share_order= "True",
            share_stock= "False",
            active= "True",
            deleted= "False")
        self.shop= Shop.objects.create(
            id_shop= "1",
            id_shop_group= self.shopgroup,
            name="Nombre"
        )
        self.producto=Product.objects.create(
            id_product="1",
            id_category_default= self.categoria,
            id_shop_default= self.shop,
            name="Nombre",
            on_sale="True",
            online_only= "True",
            quantity= 0,
            minimal_quantity= 0,
            price= 1,
            wholesale_price= 0,
            unit_price_ratio= 0,
            additional_shipping_cost=1,
            width=1,
            height=1,
            depth=1,
            weight=1,
            out_of_stock= 0,
            available_for_order="True",
            available_date= "2018-07-29",
            condition= "new",
            visibility= "everywhere",
            is_virtual="True",
            date_add= timezone.now(),
            date_upd= timezone.now()
        )

    '''Caso de prueba para verificar que se crea una categoria de un producto'''
    def test_categoryproduct_crear(self):
        form_data = {
            'id_product':self.producto.id_product,
            'id_category' : self.categoria.id_category,
            'position':1
        }
        form = CategoryProductForm(data=form_data)
        form.save()
        group1 = CategoryProduct.objects.get(id_product = "1")
        self.assertEqual(group1.id_product.name, "Nombre")
    
    '''Caso de prueba para verificar que se elimina una categoria de un producto'''
    def test_categoryproduct_eliminar(self):
        form_data = {
            'id_product':self.producto.id_product,
            'id_category' : self.categoria.id_category,
            'position':1
        }
        form = CategoryProductForm(data=form_data)
        form.save()
        group1 = CategoryProduct.objects.get(id_product = "1").delete()
        try:
            group1 = CategoryProduct.objects.get(id_product = "1")
        except:
            pass

    '''Caso de prueba para verificar que se crea una categoria de un  
        producto sin foranea'''
    def test_categoryproduct_sin_foranea(self):
        form_data = {
            'id_category' : self.categoria.id_category,
            'position':1
        }
        form = CategoryProductForm(data=form_data)
        self.assertFalse(form.is_valid())

    '''Caso de prueba para verificar si se crea una categoria de un  
        producto con foranea mala'''
    def test_categoryproduct_foranea_mala(self):
        form_data = {
            'id_product':"mala",
            'id_category' : self.categoria.id_category,
            'position':1
        }
        form = CategoryProductForm(data=form_data)
        self.assertFalse(form.is_valid())

    '''Caso de prueba para verificar si se crea una categoria de un  
        producto con position negativo'''
    def test_categoryproduct_position_negativo(self):
        form_data = {
            'id_product':self.producto.id_product,
            'id_category' : self.categoria.id_category,
            'position':-1
        }
        form = CategoryProductForm(data=form_data)
        self.assertFalse(form.is_valid())


class CategoryShopTestCase(TestCase):
    ''' Pruebas para la tabla de CategoryShop '''

    def setUp(self):
        self.categoria = Category.objects.create(
            id_category= "1",
            name="Nombre",
            description= "Description",
            level_depth= 0,
            active= "True",
            date_add= timezone.now(),
            date_upd= timezone.now(),
            position= 1,
            is_root_category= "False"
        )
        self.shopgroup = ShopGroup.objects.create(
            id_shop_group="2",
            name="Nombre grupo",
            share_order= "True",
            share_stock= "False",
            active= "True",
            deleted= "False")
        self.shop= Shop.objects.create(
            id_shop= "1",
            id_shop_group= self.shopgroup,
            name="Nombre"
        )

    '''Caso de prueba para verificar que se crea una categoria de una tienda'''
    def test_categoryshop_crear(self):
        form_data = {
            'id_shop':self.shop.id_shop,
            'id_category' : self.categoria.id_category,
            'position':1
        }
        form = CategoryShopForm(data=form_data)
        form.save()
        group1 = CategoryShop.objects.get(id_shop = "1")
        self.assertEqual(group1.id_shop.name, "Nombre")
    
    '''Caso de prueba para verificar que se elimina una categoria de una tienda'''
    def test_categoryshop_eliminar(self):
        form_data = {
            'id_shop':self.shop.id_shop,
            'id_category' : self.categoria.id_category,
            'position':1
        }
        form = CategoryShopForm(data=form_data)
        form.save()
        group1 = CategoryShop.objects.get(id_shop = "1").delete()
        try:
            group1 = CategoryShop.objects.get(id_shop = "1")
        except:
            pass

    '''Caso de prueba para verificar que se crea una categoria de una  
        tienda sin foranea'''
    def test_categoryshop_sin_foranea(self):
        form_data = {
            'id_category' : self.categoria.id_category,
            'position':1
        }
        form = CategoryShopForm(data=form_data)
        self.assertFalse(form.is_valid())

    '''Caso de prueba para verificar si se crea una categoria de una  
        tienda con foranea mala'''
    def test_categoryshop_foranea_mala(self):
        form_data = {
            'id_shop':"mala",
            'id_category' : self.categoria.id_category,
            'position':1
        }
        form = CategoryShopForm(data=form_data)
        self.assertFalse(form.is_valid())

    '''Caso de prueba para verificar si se crea una categoria de una 
        tienda con position negativo'''
    def test_categoryshop_position_negativo(self):
        form_data = {
            'id_shop':self.shop.id_shop,
            'id_category' : self.categoria.id_category,
            'position':-1
        }
        form = CategoryShopForm(data=form_data)
        self.assertFalse(form.is_valid())

class ProductAttributeTestCase(TestCase):
    ''' Pruebas para la tabla de ProductAttribute '''

    def setUp(self):
        self.categoria = Category.objects.create(
            id_category= "1",
            name="Nombre",
            description= "Description",
            level_depth= 0,
            active= "True",
            date_add= timezone.now(),
            date_upd= timezone.now(),
            position= 1,
            is_root_category= "False"
        )
        self.shopgroup = ShopGroup.objects.create(
            id_shop_group="2",
            name="Nombre grupo",
            share_order= "True",
            share_stock= "False",
            active= "True",
            deleted= "False")
        self.shop= Shop.objects.create(
            id_shop= "1",
            id_shop_group= self.shopgroup,
            name="Nombre"
        )
        self.producto=Product.objects.create(
            id_product="1",
            id_category_default= self.categoria,
            id_shop_default= self.shop,
            name="Nombre",
            on_sale="True",
            online_only= "True",
            quantity= 0,
            minimal_quantity= 0,
            price= 1,
            wholesale_price= 0,
            unit_price_ratio= 0,
            additional_shipping_cost=1,
            width=1,
            height=1,
            depth=1,
            weight=1,
            out_of_stock= 0,
            available_for_order="True",
            available_date= "2018-07-29",
            condition= "new",
            visibility= "everywhere",
            is_virtual="True",
            date_add= timezone.now(),
            date_upd= timezone.now()
        )

    '''Caso de prueba para verificar que se crea una atributo de un producto'''
    def test_productattribute_crear(self):
        form_data = {
            'id_product_attribute' :1,
            'id_product':self.producto.id_product,
            'wholesale_price':1,
            'price': 1,
            'quantity':1,
            'weight':1,
            'unit_price_impact':1,
            'minimal_quantity':1,
            'available_date': "2018-07-29"
        }
        form = ProductAttributeForm(data=form_data)
        form.save()
        group1 = ProductAttribute.objects.get(id_product = "1")
        self.assertEqual(group1.id_product.name, "Nombre")
    
    '''Caso de prueba para verificar que se elimina un atributo de un producto'''
    def test_productattribute_eliminar(self):
        form_data = {
            'id_product_attribute' :1,
            'id_product':self.producto.id_product,
            'wholesale_price':1,
            'price': 1,
            'quantity':1,
            'weight':1,
            'unit_price_impact':1,
            'minimal_quantity':1,
            'available_date': "2018-07-29"
        }
        form = ProductAttributeForm(data=form_data)
        form.save()
        group1 = ProductAttribute.objects.get(id_product = "1").delete()
        try:
            group1 = ProductAttribute.objects.get(id_product = "1")
        except:
            pass

    '''Caso de prueba para verificar que se edita un atributo de un producto'''
    def test_productattribute_editar(self):
        form_data = {
            'id_product_attribute' :1,
            'id_product':self.producto.id_product,
            'wholesale_price':1,
            'price': 1,
            'quantity':1,
            'weight':1,
            'unit_price_impact':1,
            'minimal_quantity':1,
            'available_date': "2018-07-29"
        }
        form = ProductAttributeForm(data=form_data)
        form.save()
        shop1 = ProductAttribute.objects.get(price = 1)
        shop1.price=2
        shop1.save()
        shop1 = ProductAttribute.objects.get(price = 2)
        self.assertEqual(shop1.price, 2)
    
    '''Caso de prueba para verificar si se crea un atributo de un producto
        con precio negativo'''
    def test_productattribute_precio_negativo(self):
        form_data = {
            'id_product_attribute' :1,
            'id_product':self.producto.id_product,
            'wholesale_price':1,
            'price': -1,
            'quantity':1,
            'weight':1,
            'unit_price_impact':1,
            'minimal_quantity':1,
            'available_date': "2018-07-29"
        }
        form = ProductAttributeForm(data=form_data)
        self.assertFalse(form.is_valid())

    '''Caso de prueba para verificar si se crea un atributo de un producto
        con string vacio de fecha'''
    def test_productattribute_sin_fecha(self):
        form_data = {
            'id_product_attribute' :1,
            'id_product':self.producto.id_product,
            'wholesale_price':1,
            'price': 1,
            'quantity':1,
            'weight':1,
            'unit_price_impact':1,
            'minimal_quantity':1,
            'available_date': ""
        }
        form = ProductAttributeForm(data=form_data)
        self.assertFalse(form.is_valid())