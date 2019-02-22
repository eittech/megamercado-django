from django.contrib import admin

# Register your models here.
from customers.models import *

admin.site.register(Customer)
admin.site.register(AddressCustomer)
