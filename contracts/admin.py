from django.contrib import admin

# Register your models here.
from contracts.models import *


class ServiceContractInline(admin.TabularInline):
    model = ServiceContract
    extra = 1

class ContractsAdmin(admin.ModelAdmin):
    inlines = (ServiceContractInline,)

admin.site.register(ServiceContract)

admin.site.register(Contracts,ContractsAdmin)
admin.site.register(Payment)
admin.site.register(InvoiceContract)
