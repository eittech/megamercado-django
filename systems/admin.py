from django.contrib import admin
from .models import *
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
import json

# Register your models here.
class RegisterActivitySystemAdmin(admin.ModelAdmin):
    list_filter = ('type','template_section','country_name','region_name',
    ('user',admin.RelatedOnlyFieldListFilter),
    ('shop',admin.RelatedOnlyFieldListFilter),
    ('category',admin.RelatedOnlyFieldListFilter))
    list_display = ('type','datet','word_search','shop','template_section','category')
    date_hierarchy = 'datet'

    @mark_safe
    def word_search(self, obj):
        data = obj.data.replace("\'", "\"")
        data = json.loads(data)
        return u'%' % (data['texto'])
        # u'<img src="%s" alt="thumbnail: %s" width="%d" height="%d"/>' % (thumb.url, obj.photo.name, thumb.width, thumb.height)
    word_search.short_description = 'Palabras buscadas'
    word_search.allow_tags = True

    readonly_fields = ['type','user','data','shop','product','category','template_section','location',
    'continent_name','country_name','region_name','zip','latitude','longitude']
    save_as = True
    save_on_top = True
    change_list_template = 'admin/change_list_register_activity_graph.html'
    def get_queryset(self, request):
        user = request.user
        if user.is_superuser:
            queryset = super().get_queryset(request)
        else:
            customer = Customer.objects.get(user=user)
            shop = Shop.objects.filter(customer=customer)
            # print(shop)
            queryset = RegisterActivitySystem.objects.filter(shop__in=shop)
        return queryset
    class Meta:
        app_label = "sistemas"
    # readonly_fields = ['category','category_temp','photo']
    # search_fields = ['name']
admin.site.title = _("sistemas admin")
admin.site.register(RegisterActivitySystem,RegisterActivitySystemAdmin)
admin.site.register(ContactMessage)
