from django.contrib import admin
from .models import *
# Register your models here.
class RegisterActivitySystemAdmin(admin.ModelAdmin):
    list_filter = ('type',('user',admin.RelatedOnlyFieldListFilter))
    list_display = ('type', 'user','datet')
    date_hierarchy = 'datet'
    # readonly_fields = ['category','category_temp','photo']
    # search_fields = ['name']
admin.site.register(RegisterActivitySystem,RegisterActivitySystemAdmin)
admin.site.register(ContactMessage)
