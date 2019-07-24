from django.contrib import admin
from currency.models import *
# Register your models here.

class CurrencyAdmin(admin.ModelAdmin):
	list_display = ['id_currency', 'name','iso_code','iso_code_num','sign','decimals','icono','deleted', 'active']

class CurrencyRefAdmin(admin.ModelAdmin):
	list_display = ['id_currency', 'id_shop','publish']

class CurrencyShopAdmin(admin.ModelAdmin):
	list_display = ['id_currency', 'id_shop','rate_moneda','rate_referencia']

class AccountAdmin(admin.ModelAdmin):
	list_display = ['id_account','id_currency','name','tipo','number','owner','persona']

# Monedas
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(CurrencyRef, CurrencyRefAdmin)
admin.site.register(CurrencyShop, CurrencyShopAdmin)

admin.site.register(Account, AccountAdmin)