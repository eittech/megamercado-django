from django.contrib import admin
from .models import *
from django.utils.translation import ugettext_lazy as _
# Register your models here.
class RegisterActivitySystemAdmin(admin.ModelAdmin):
    list_filter = ('type',('user',admin.RelatedOnlyFieldListFilter))
    list_display = ('type', 'user','datet')
    date_hierarchy = 'datet'
    readonly_fields = ['type','user','data']
    class Meta:
        app_label = "sistemas"
    # readonly_fields = ['category','category_temp','photo']
    # search_fields = ['name']
admin.site.title = _("sistemas admin")
admin.site.register(RegisterActivitySystem,RegisterActivitySystemAdmin)
admin.site.register(ContactMessage)
