from django.conf import settings
from products.models import *
import csv

settings.BASE_DIR


#kits
kits = Category.objects.create(name="Kits",slug="kits")
control = Category.objects.create(name="Control",slug="control")
cultivo = Category.objects.create(name="Cultivo",slug="cultivo")
indoor = Category.objects.create(name="Indoor",slug="indoor")
parafernalia = Category.objects.create(name="Parafernalia",slug="parafernalia")

if kits:
    Category.objects.create(name="Kit Cultivo",slug="kit-cultivo",parent=kits)
    Category.objects.create(name="Kit Sustratos",slug="kit-sustratos",parent=kits)
    Category.objects.create(name="Kit Semillas",slug="kit-semillas",parent=kits)
    Category.objects.create(name="Kit Fertilizantes",slug="kit-fertilizantes",parent=kits)
    Category.objects.create(name="Kit Iluminación",slug="kit-iluminacion",parent=kits)
    Category.objects.create(name="Kit Ventilación",slug="kit-entilacion",parent=kits)
    Category.objects.create(name="Kit Control",slug="kit-control",parent=kits)
    Category.objects.create(name="Kit Herramientas",slug="kit-herramientas",parent=kits)

if control:
    ccultivo = Category.objects.create(name="Control Cultivo",slug="control-cultivo",parent=control)
    if ccultivo:
        Category.objects.create(name="Ph y Ec",slug="ph-ec",parent=ccultivo)
        Category.objects.create(name="Temperatura",slug="temperatura",parent=ccultivo)
        Category.objects.create(name="CO2",slug="co2",parent=ccultivo)
        Category.objects.create(name="Riego",slug="riego",parent=ccultivo)
        Category.objects.create(name="Humedad",slug="humedad",parent=ccultivo)
        Category.objects.create(name="Temporizadores",slug="temporizadores",parent=ccultivo)

if cultivo:
    Category.objects.create(name="Macetas",slug="macetas",parent=cultivo)
    Category.objects.create(name="Sustratos",slug="sustratos",parent=cultivo)
    semillas = Category.objects.create(name="Semillas",slug="semillas",parent=cultivo)
    if semillas:
        Category.objects.create(name="Autoflorecientes",slug="autoflorecientes",parent=semillas)
        Category.objects.create(name="Feminizadas",slug="feminizadas",parent=semillas)
        Category.objects.create(name="Medicinales",slug="medicinales",parent=semillas)
    Category.objects.create(name="Fertilizantes",slug="fertilizantes",parent=cultivo)
    Category.objects.create(name="Herramientas Cultivo",slug="herramientas-cultivo",parent=cultivo)
    Category.objects.create(name="Control Plagas",slug="control-plagas",parent=cultivo)

if indoor:
    iluminacion = Category.objects.create(name="Iluminación",slug="iluminacion",parent=indoor)
    if iluminacion:
        Category.objects.create(name="LED",slug="led",parent=iluminacion)
        Category.objects.create(name="Sodio",slug="sodio",parent=iluminacion)
        Category.objects.create(name="Haluro",slug="haluro",parent=iluminacion)
        Category.objects.create(name="Bajo Consumo",slug="bajo-consumo",parent=iluminacion)
    Category.objects.create(name="Reflectores",slug="reflectores",parent=indoor)
    Category.objects.create(name="Ballasts",slug="ballasts",parent=indoor)
    Category.objects.create(name="Carpas",slug="carpas",parent=indoor)
    ventilacion = Category.objects.create(name="Ventilación",slug="ventilacion",parent=indoor)
    if ventilacion:
        Category.objects.create(name="Ventiladores",slug="ventiladores",parent=ventilacion)
        Category.objects.create(name="Extractores",slug="extractores",parent=ventilacion)
        Category.objects.create(name="Ductos",slug="ductos",parent=ventilacion)
        Category.objects.create(name="Control Olor",slug="control-olor",parent=ventilacion)

if parafernalia:
    Category.objects.create(name="Vaporizadores",slug="vaporizadores",parent=parafernalia)
    Category.objects.create(name="Pipas",slug="pipas",parent=parafernalia)
    Category.objects.create(name="Bongs",slug="bongs",parent=parafernalia)
    Category.objects.create(name="Moledores",slug="moledores",parent=parafernalia)
    Category.objects.create(name="Enroladores",slug="enroladores",parent=parafernalia)
    Category.objects.create(name="Papelillos",slug="papelillos",parent=parafernalia)
    Category.objects.create(name="Encendedores",slug="encendedores",parent=parafernalia)

with open('t.csv', 'r+') as data_file:
    data = csv.reader(data_file, delimiter=',')
    for row in data:
        resultado = Category.objects.filter(name=row[1])
        if resultado:
            categoria = None
            for item in resultado:
                categoria = item
            catg=CategoryTags.objects.create(category=categoria,tag=str(row[0]))
            if catg:
                print("grabado")
            # print(categoria)
            # print(row)
