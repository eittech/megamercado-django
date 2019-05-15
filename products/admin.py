from django.contrib import admin
from products.models import *
from customers.models import *
# Register your models here.
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAttributesInline(admin.TabularInline):
    model = ProductAttributes
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_filter = ('photo',('shop',admin.RelatedOnlyFieldListFilter), ('category',admin.RelatedOnlyFieldListFilter))
    list_display = ('name', 'price','tax','total')
    # readonly_fields = ['category','category_temp','photo']
    search_fields = ['name']
    # date_hierarchy = 'shop'
    inlines = (ProductAttributesInline,ProductImageInline)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "shop":
            user = request.user
            if user.is_superuser:
                kwargs["queryset"] = Shop.objects.all()
            else:
                customer = Customer.objects.get(user=user)
                # shop = Shop.objects.filter(customer=customer)
                kwargs["queryset"] = Shop.objects.filter(customer=customer)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        user = request.user
        if user.is_superuser:
            queryset = super().get_queryset(request)
        else:
            print(user)
            customer = Customer.objects.get(user=user)
            print(customer)
            shop = Shop.objects.filter(customer=customer)
            # print(shop)
            queryset = Product.objects.filter(shop__in=shop)
            print('hola admin')
        return queryset


class CategoryTagsInline(admin.TabularInline):
    model = CategoryTags
    extra = 1

class CategoryAdmin(DraggableMPTTAdmin):
    inlines = (CategoryTagsInline,)
    prepopulated_fields = {"slug": ("name",)}
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title')
    list_display_links = ('indented_title',)

class ShopAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }
    list_display = ('name', 'num_products','num_products_category','num_products_category_null')
    search_fields = ['name',]
    readonly_fields = ['customer','url']
    def get_queryset(self, request):
        user = request.user
        if user.is_superuser:
            queryset = super().get_queryset(request)
        else:
            print(user)
            customer = Customer.objects.get(user=user)
            print(customer)
            # shop = Shop.objects.filter(customer=customer)
            # print(shop)
            queryset = Shop.objects.filter(customer=customer)
        return queryset

class HistoryPriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'date_update','total')

class AlertsProductAdmin(admin.ModelAdmin):
    list_display = ('product','type')

class ListCategoryTaxAdmin(admin.ModelAdmin):
    list_display = ('tag','state')

admin.site.register(ListCategoryTax,ListCategoryTaxAdmin)










admin.site.register(AlertsProduct,AlertsProductAdmin)


admin.site.register(HistoryPrice,HistoryPriceAdmin)
admin.site.register(Shop,ShopAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)

class ProductImageAdmin(admin.ModelAdmin):
    list_filter = (('product__shop',admin.RelatedOnlyFieldListFilter), ('product__category',admin.RelatedOnlyFieldListFilter))
    list_display = ('product', 'image')
    readonly_fields = ['product',]
    search_fields = ['product__name']
    # inlines = (ProductAttributesInline,ProductImageInline)
    def get_queryset(self, request):
        user = request.user
        if user.is_superuser:
            queryset = super().get_queryset(request)
        else:
            print(user)
            customer = Customer.objects.get(user=user)
            print(customer)
            shop = Shop.objects.filter(customer=customer)
            # print(shop)
            queryset = ProductImage.objects.filter(product__shop__in=shop)
            print('hola admin')
        return queryset
# admin.site.register(ProductImage,ProductImageAdmin)
admin.site.register(Attributes)
admin.site.register(ProductAttributes)
admin.site.register(FavoriteProduct)
admin.site.register(FavoriteBrands)
admin.site.register(FavoriteSearchs)


def controlaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=2)
        queryset.update(category=category)
controlaction.short_description = "Control"
def co2action(modeladmin, request, queryset):
        category = Category.objects.get(pk=17)
        queryset.update(category=category)
co2action.short_description = "CO2"
def humedadaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=19)
        queryset.update(category=category)
humedadaction.short_description = "Humedad"
def phecaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=15)
        queryset.update(category=category)
phecaction.short_description = "Ph y Ec"
def riegoaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=18)
        queryset.update(category=category)
riegoaction.short_description = "Riego"
def temperaturaaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=16)
        queryset.update(category=category)
temperaturaaction.short_description = "Temperatura"
def temporizadoresaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=20)
        queryset.update(category=category)
temporizadoresaction.short_description = "Temporizadores"
def cultivoaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=3)
        queryset.update(category=category)
cultivoaction.short_description = "Cultivo"
def controlplagasaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=29)
        queryset.update(category=category)
controlplagasaction.short_description = "Control Plagas"
def fertilizantesaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=27)
        queryset.update(category=category)
fertilizantesaction.short_description = "Fertilizantes"
def herramientascultivoaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=28)
        queryset.update(category=category)
herramientascultivoaction.short_description = "Herramientas Cultivo"
def macetasaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=21)
        queryset.update(category=category)
macetasaction.short_description = "Macetas"
def semillasaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=23)
        queryset.update(category=category)
semillasaction.short_description = "Semillas"
def autoflorecientesaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=24)
        queryset.update(category=category)
autoflorecientesaction.short_description = "Autoflorecientes"
def feminizadasaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=25)
        queryset.update(category=category)
feminizadasaction.short_description = "Feminizadas"
def medicinalesaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=26)
        queryset.update(category=category)
medicinalesaction.short_description = "Medicinales"
def sustratosaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=22)
        queryset.update(category=category)
sustratosaction.short_description = "Sustratos"
def indooraction(modeladmin, request, queryset):
        category = Category.objects.get(pk=4)
        queryset.update(category=category)
indooraction.short_description = "Indoor"
def carpasaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=37)
        queryset.update(category=category)
carpasaction.short_description = "Carpas"
def iluminacionaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=30)
        queryset.update(category=category)
iluminacionaction.short_description = "Iluminación"
def ballastsaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=36)
        queryset.update(category=category)
ballastsaction.short_description = "Ballasts"
def bajoconsumoaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=34)
        queryset.update(category=category)
bajoconsumoaction.short_description = "Bajo Consumo"
def haluroaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=33)
        queryset.update(category=category)
haluroaction.short_description = "Haluro"
def ledaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=31)
        queryset.update(category=category)
ledaction.short_description = "LED"
def sodioaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=32)
        queryset.update(category=category)
sodioaction.short_description = "Sodio"
def reflectoresaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=35)
        queryset.update(category=category)
reflectoresaction.short_description = "Reflectores"
def ventilacionaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=38)
        queryset.update(category=category)
ventilacionaction.short_description = "Ventilación"
def controloloraction(modeladmin, request, queryset):
        category = Category.objects.get(pk=42)
        queryset.update(category=category)
controloloraction.short_description = "Control Olor"
def ductosaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=41)
        queryset.update(category=category)
ductosaction.short_description = "Ductos"
def extractoresaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=40)
        queryset.update(category=category)
extractoresaction.short_description = "Extractores"
def ventiladoresaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=39)
        queryset.update(category=category)
ventiladoresaction.short_description = "Ventiladores"
def kitsaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=1)
        queryset.update(category=category)
kitsaction.short_description = "Kits"
def kitcontrolaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=12)
        queryset.update(category=category)
kitcontrolaction.short_description = "Kit Control"
def kitcultivoaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=6)
        queryset.update(category=category)
kitcultivoaction.short_description = "Kit Cultivo"
def kitfertilizantesaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=9)
        queryset.update(category=category)
kitfertilizantesaction.short_description = "Kit Fertilizantes"
def kitherramientasaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=13)
        queryset.update(category=category)
kitherramientasaction.short_description = "Kit Herramientas"
def kitiluminacionaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=10)
        queryset.update(category=category)
kitiluminacionaction.short_description = "Kit Iluminación"
def kitsemillasaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=8)
        queryset.update(category=category)
kitsemillasaction.short_description = "Kit Semillas"
def kitsustratosaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=7)
        queryset.update(category=category)
kitsustratosaction.short_description = "Kit Sustratos"
def kitentilacionaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=11)
        queryset.update(category=category)
kitentilacionaction.short_description = "Kit Ventilación"
def parafernaliaaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=5)
        queryset.update(category=category)
parafernaliaaction.short_description = "Parafernalia"
def bongsaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=45)
        queryset.update(category=category)
bongsaction.short_description = "Bongs"
def encendedoresaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=49)
        queryset.update(category=category)
encendedoresaction.short_description = "Encendedores"
def enroladoresaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=47)
        queryset.update(category=category)
enroladoresaction.short_description = "Enroladores"
def moledoresaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=46)
        queryset.update(category=category)
moledoresaction.short_description = "Moledores"
def papelillosaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=48)
        queryset.update(category=category)
papelillosaction.short_description = "Papelillos"
def pipasaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=44)
        queryset.update(category=category)
pipasaction.short_description = "Pipas"
def vaporizadoresaction(modeladmin, request, queryset):
        category = Category.objects.get(pk=43)
        queryset.update(category=category)
vaporizadoresaction.short_description = "Vaporizadores"


class CategoryTagsAdmin(admin.ModelAdmin):
    list_filter = ('category',)
    list_display = ('tag','category')
    actions =[controlaction,co2action,humedadaction,phecaction,riegoaction,temperaturaaction,temporizadoresaction,cultivoaction,controlplagasaction,fertilizantesaction,herramientascultivoaction,macetasaction,semillasaction,autoflorecientesaction,feminizadasaction,medicinalesaction,sustratosaction,indooraction,carpasaction,iluminacionaction,ballastsaction,bajoconsumoaction,haluroaction,ledaction,sodioaction,reflectoresaction,ventilacionaction,controloloraction,ductosaction,extractoresaction,ventiladoresaction,kitsaction,kitcontrolaction,kitcultivoaction,kitfertilizantesaction,kitherramientasaction,kitiluminacionaction,kitsemillasaction,kitsustratosaction,kitentilacionaction,parafernaliaaction,bongsaction,encendedoresaction,enroladoresaction,moledoresaction,papelillosaction,pipasaction,vaporizadoresaction]

admin.site.register(CategoryTags,CategoryTagsAdmin)
