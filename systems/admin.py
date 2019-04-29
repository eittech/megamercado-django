from django.contrib import admin
from .models import *
from django.utils.translation import ugettext_lazy as _
# Register your models here.
class RegisterActivitySystemAdmin(admin.ModelAdmin):
    list_filter = ('type','template_section',
    ('user',admin.RelatedOnlyFieldListFilter),
    ('shop',admin.RelatedOnlyFieldListFilter),
    ('category',admin.RelatedOnlyFieldListFilter),
    ('product',admin.RelatedOnlyFieldListFilter))
    list_display = ('type','datet','shop','template_section','category')
    date_hierarchy = 'datet'
    readonly_fields = ['type','user','data','shop','product','category','template_section']
    save_as = True
    save_on_top = True
    change_list_template = 'admin/change_list_register_activity_graph.html'
    class Meta:
        app_label = "sistemas"
    # readonly_fields = ['category','category_temp','photo']
    # search_fields = ['name']
admin.site.title = _("sistemas admin")
admin.site.register(RegisterActivitySystem,RegisterActivitySystemAdmin)
admin.site.register(ContactMessage)
