from django.contrib import admin

# Register your models here.
from customers.models import *

class CustomerAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            user = request.user
            if user.is_superuser:
                kwargs["queryset"] = Customer.objects.all()
            else:
                kwargs["queryset"] = User.objects.filter(username=user.username)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def get_queryset(self, request):
        user = request.user
        if user.is_superuser:
            queryset = super().get_queryset(request)
        else:
            customer = Customer.objects.filter(user=user)
            # shop = Shop.objects.filter(customer=customer)
            queryset = customer
        return queryset
        # readonly_fields = ['category','category_temp','photo']
    # def get_readonly_fields(self, db_field,request, obj=None):
    #     ro_fields = super(CustomerAdmin, self).get_readonly_fields(request, obj)
    #     print(db_field.name)
    #     # if not 'user' in ro_fields:
    #     #     ro_fields.append('user')
    #     return ro_fields
admin.site.register(Customer,CustomerAdmin)

class AddressCustomerAdmin(admin.ModelAdmin):
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
            addresscustomer = AddressCustomer.objects.filter(customer=customer)
            queryset = addresscustomer
        return queryset

admin.site.register(AddressCustomer,AddressCustomerAdmin)

class MailVerificationAdmin(admin.ModelAdmin):
    list_filter = ('type',)
    list_display = ('user', 'token','type')
    search_fields = ['user__firts_name']
admin.site.register(MailVerification,MailVerificationAdmin)
