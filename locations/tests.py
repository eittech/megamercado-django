from django.test import TestCase
from locations.models import *
from locations.forms import *

# Create your tests here.
class ZoneTestCase(TestCase):
    ''' Pruebas para la tabla de ShopGroup '''

    def setUp(self):
        pass

    '''Caso de prueba para verificar que se crea una zona'''
    def test_zone_crear(self):
        form_data = {
            'id_zone': "1",
            'name' : "Nombre",
            'active': "True"
        }
        form = ZoneForm(data=form_data)
        form.save()
        group1 = Zone.objects.get(name = "Nombre")
        self.assertEqual(group1.name, "Nombre")

    '''Caso de prueba para verificar que se elimina una zona'''
    def test_zone_eliminar(self):
        form_data = {
            'id_zone': "1",
            'name' : "Nombre",
            'active': "True"
        }
        form = ZoneForm(data = form_data)
        form.save()
        group1 = Zone.objects.get(name = "Nombre").delete()
        try:
            group1 = Zone.objects.get(name = "Nombre")
        except:
            pass

    '''Caso de prueba para verificar que se edita una zona'''
    def test_zone_editar(self):
        form_data = {
            'id_zone': "1",
            'name' : "Nombre",
            'active': "True"
        }
        form = ZoneForm(data=form_data)
        form.save()
        shop1 = Zone.objects.get(name = "Nombre")
        shop1.name="Change"
        shop1.save()
        shop1 = Zone.objects.get(name = "Change")
        self.assertEqual(shop1.name, "Change")

    ''' Caso de prueba para verificar si se añaden instancias que poseen strings vacios en
        el nombre de la zona. '''
    def test_shopgroup_sin_name(self):
        form_data = {
            'id_zone': "1",
            'name' : "",
            'active': "True"
        }
        form = ZoneForm(data=form_data)
        self.assertFalse(form.is_valid())

class CountryTestCase(TestCase):
    ''' Pruebas para la tabla de ShopGroup '''

    def setUp(self):
        self.zone= Zone.objects.create(
            id_zone= "1",
            name= "Nombre",
            active= "True"
        )

    '''Caso de prueba para verificar que se crea un pais'''
    def test_country_crear(self):
        form_data = {
            'id_country' : "1",
            'id_zone': self.zone.id_zone,
            'name' : "Nombre",
            'iso_code': "626",
            'call_prefix': 23,
            'zip_code_format' : "www"
        }
        form = CountryForm(data=form_data)
        form.save()
        shop1 = Country.objects.get(name = "Nombre")
        self.assertEqual(shop1.name, "Nombre")
    
    '''Caso de prueba para verificar que se elimina un pais'''
    def test_country_eliminar(self):
        form_data = {
            'id_country' : "1",
            'id_zone': self.zone.id_zone,
            'name' : "Nombre",
            'iso_code': "626",
            'call_prefix': 23,
            'zip_code_format' : "www"
        }
        form = CountryForm(data=form_data)
        form.save()
        shop1 = Country.objects.get(name = "Nombre").delete()
        try:
            shop1 = Country.objects.get(name = "Nombre")
        except:
            pass

    '''Caso de prueba para verificar que se edita un pais'''
    def test_country_editar(self):
        form_data = {
            'id_country' : "1",
            'id_zone': self.zone.id_zone,
            'name' : "Nombre",
            'iso_code': "626",
            'call_prefix': 23,
            'zip_code_format' : "www"
        }
        form = CountryForm(data=form_data)
        form.save()
        shop1 = Country.objects.get(name = "Nombre")
        shop1.name="Change"
        shop1.save()
        shop1 = Country.objects.get(name = "Change")
        self.assertEqual(shop1.name, "Change")

    '''Caso de prueba para verificar si se crea un pais sin nombre'''
    def test_country_sin_name(self):
        form_data = {
            'id_country' : "1",
            'id_zone': self.zone.id_zone,
            'name' : "",
            'iso_code': "626",
            'call_prefix': 23,
            'zip_code_format' : "www"
        }
        form = CountryForm(data=form_data)
        self.assertFalse(form.is_valid())

    '''Caso de prueba para verificar si se crea un pais sin foranea'''
    def test_country_sin_foranea(self):
        form_data = {
            'id_country' : "1",
            'name' : "Nombre",
            'iso_code': "626",
            'call_prefix': 23,
            'zip_code_format' : "www"
        }
        form = CountryForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    '''Caso de prueba para verificar si se crea un pais con foranea mala'''
    def test_country_foranea_mala(self):
        form_data = {
            'id_country' : "1",
            'id_zone': "mala",
            'name' : "Nombre",
            'iso_code': "626",
            'call_prefix': 23,
            'zip_code_format' : "www"
        }
        form = CountryForm(data=form_data)
        self.assertFalse(form.is_valid())

class CountryShopTestCase(TestCase):
    ''' Pruebas para la tabla de CountryShop '''

    def setUp(self):
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
        self.zone= Zone.objects.create(
            id_zone= "1",
            name= "Nombre",
            active= "True"
        )
        self.country=Country.objects.create(
            id_country= "1",
            id_zone= self.zone,
            name="Nombre",
            contains_states =False,
            iso_code="626",
            call_prefix= 23,
            zip_code_format= "www"
        )

    '''Caso de prueba para verificar que se crea una categoria de una tienda'''
    def test_counrtyshop_crear(self):
        form_data = {
            'id_shop':self.shop.id_shop,
            'id_country' : self.country.id_country
        }
        form = CountryShopForm(data=form_data)
        form.save()
        group1 = CountryShop.objects.get(id_shop = "1")
        self.assertEqual(group1.id_shop.name, "Nombre")
    
    '''Caso de prueba para verificar que se elimina una categoria de una tienda'''
    def test_countryshop_eliminar(self):
        form_data = {
            'id_shop':self.shop.id_shop,
            'id_country' : self.country.id_country
        }
        form = CountryShopForm(data=form_data)
        form.save()
        group1 = CountryShop.objects.get(id_shop = "1").delete()
        try:
            group1 = CountryShop.objects.get(id_shop = "1")
        except:
            pass

    '''Caso de prueba para verificar que se crea un pais de una  
        tienda sin foranea'''
    def test_countryshop_sin_foranea(self):
        form_data = {
            'id_country' : self.country.id_country
        }
        form = CountryShopForm(data=form_data)
        self.assertFalse(form.is_valid())

    '''Caso de prueba para verificar si se crea un pais de una  
        tienda con foranea mala'''
    def test_countryshop_foranea_mala(self):
        form_data = {
            'id_shop':"mala",
            'id_country' : self.country.id_country
        }
        form = CountryShopForm(data=form_data)
        self.assertFalse(form.is_valid())
