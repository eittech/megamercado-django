from django.contrib import admin
from carrier.models import *
# Register your models here.

class CarrierAdmin(admin.ModelAdmin):
	list_display = ['id_carrier', 'name']


# Transportistas
admin.site.register(Carrier, CarrierAdmin)