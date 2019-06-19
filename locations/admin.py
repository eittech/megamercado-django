from django.contrib import admin
from locations.models import *

# Register your models here.

class StateInline(admin.TabularInline):
    model = State
    extra = 1

class AddressInline(admin.TabularInline):
    model = Address
    extra = 1

class CountryInline(admin.TabularInline):
    model = Country
    extra = 1

class CountryShopInline(admin.TabularInline):
    model = CountryShop
    extra = 1

class ZoneAdmin(admin.ModelAdmin):
    list_display = ['id_zone', 'name', 'active']
    inlines=[CountryInline,]

class CountryAdmin(admin.ModelAdmin):
    list_display = ['id_country', 'name','id_zone', 'iso_code',  'active']
    inlines=[StateInline,CountryShopInline,]

class StateAdmin(admin.ModelAdmin):
    list_display = ['id_state', 'id_country', 'name','iso_code','tax_behavior', 'active']
    inlines=[AddressInline,]

class CountryShopAdmin(admin.ModelAdmin):
    list_display = ['id_country', 'id_shop']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['id_address' ,'id_country', 'id_state','id_customer','address1', 'address2', 'postcode', 'active', 'deleted']

admin.site.register(Zone, ZoneAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(CountryShop,CountryShopAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Address,AddressAdmin)