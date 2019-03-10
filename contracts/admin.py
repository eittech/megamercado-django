from django.contrib import admin

# Register your models here.
from contracts.models import *


class ServiceContractInline(admin.TabularInline):
    model = ServiceContract
    extra = 1

class ContractsAdmin(admin.ModelAdmin):
    inlines = (ServiceContractInline,)

class ServiceContractProductInline(admin.TabularInline):
    model = ServiceContractProduct
    extra = 1

class ServiceContractShopInline(admin.TabularInline):
    model = ServiceContractShop
    extra = 1

class ServiceContractAdmin(admin.ModelAdmin):
    inlines = (ServiceContractProductInline,ServiceContractShopInline,)

admin.site.register(ServiceContract,ServiceContractAdmin)

admin.site.register(Contracts,ContractsAdmin)
admin.site.register(Payment)
admin.site.register(InvoiceContract)
