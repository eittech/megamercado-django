from django.contrib import admin
from locations.models import *

# Register your models here.
admin.site.register(Zone)
admin.site.register(Country)
admin.site.register(CountryShop)
admin.site.register(State)
admin.site.register(Address)