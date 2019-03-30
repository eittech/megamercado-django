from django.contrib import admin

# Register your models here.
from customers.models import *

admin.site.register(Customer)
admin.site.register(AddressCustomer)

class MailVerificationAdmin(admin.ModelAdmin):
    list_filter = ('type',)
    list_display = ('user', 'token','type')
    search_fields = ['user__firts_name']
admin.site.register(MailVerification,MailVerificationAdmin)
