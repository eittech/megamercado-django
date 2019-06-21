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