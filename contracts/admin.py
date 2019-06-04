from django.contrib import admin

# Register your models here.
from contracts.models import *
from customers.models import *
from django.utils.safestring import mark_safe


class ServiceContractInline(admin.TabularInline):
    model = ServiceContract
    extra = 1



class ContractsAdmin(admin.ModelAdmin):
    inlines = (ServiceContractInline,)
    list_display = ('id','customer','date_contract','total','state_contract')
    change_list_template = 'admin/change_list_contract.html'
    @mark_safe
    def state_contract(self, obj):
        return u'<i class="fas fa-file-alt" style="font-size: 16px;color: brown;margin-right: 10px;"></i> <i class="fas fa-file-invoice-dollar" style="font-size: 16px;color: brown;margin-right: 10px;"></i> <a class="%s">%s</a>' % (obj.state,obj.get_state_display())
        # u'<img src="%s" alt="thumbnail: %s" width="%d" height="%d"/>' % (thumb.url, obj.photo.name, thumb.width, thumb.height)
    state_contract.short_description = 'Estado'
    state_contract.allow_tags = True
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "customer":
            user = request.user
            if user.is_superuser:
                kwargs["queryset"] = Customer.objects.all()
            else:
                kwargs["queryset"] = Customer.objects.filter(user=user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def get_queryset(self, request):
        user = request.user
        if user.is_superuser:
            queryset = super().get_queryset(request)
        else:
            customer = Customer.objects.get(user=user)
            # shop = Shop.objects.filter(customer=customer)
            # print(shop)
            queryset = Contracts.objects.filter(customer=customer)
        return queryset


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


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1

class InvoiceContractAdmin(admin.ModelAdmin):
    # inlines = (ServiceContractInline,)
    inlines = (PaymentInline,)
    list_display = ('number','contract','date_invoice','amount','tax','total')
admin.site.register(InvoiceContract,InvoiceContractAdmin)
