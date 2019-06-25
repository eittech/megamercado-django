from django.contrib import admin
from products.models import *
from customers.models import *
# Register your models here.
#cambio test 223
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

from django.utils.safestring import mark_safe

class ShopInline(admin.TabularInline):
	model = Shop
	extra = 1

class CategoryGroupInline(admin.TabularInline):
	model = CategoryGroup
	extra = 1

class CategoryShopInline(admin.TabularInline):
	model = CategoryShop
	extra = 1

class AttributeGroupShopInline(admin.TabularInline):
	model = AttributeGroupShop
	extra = 1

class AttributeShopInline(admin.TabularInline):
	model = AttributeShop
	extra = 1

class ProductAttributeCombinationInline(admin.TabularInline):
	model = ProductAttributeCombination
	extra = 1

class ProductAttributeShopInline(admin.TabularInline):
	model = ProductAttributeShop
	extra = 1

class CategoryProductInline(admin.TabularInline):
	model = CategoryProduct
	extra = 1

class AttributeImpactInline(admin.TabularInline):
	model = AttributeImpact
	extra = 1

class ProductAttributeImageInline(admin.TabularInline):
	model = ProductAttributeImage
	extra= 1

class ShopGroupAdmin(admin.ModelAdmin):
	list_display = ['id_shop_group', 'name','share_order','share_stock','active','deleted']
	inlines=[ShopInline,]

class ShopAdmin(admin.ModelAdmin):
	list_display = ['id_shop', 'id_shop_group', 'name', 'active', 'deleted','virtual_url']
	inlines=[CategoryShopInline, ]

class CategoryShopAdmin(admin.ModelAdmin):
	list_display = ['id_category','id_shop', 'position']

class GroupsAdmin(admin.ModelAdmin):
	list_display = ['id_group', 'name', 'reduction','price_display_method','show_prices','date_add', 'date_upd']
	inlines=[CategoryGroupInline,]

class CategoryGroupAdmin(admin.ModelAdmin):
	list_display = ['id_category', 'id_group']

class CategoryAdmin(admin.ModelAdmin):
	list_display = ['id_category', 'name','description','id_parent','level_depth','active','date_add','date_upd', 'position']

class AttributeGroupAdmin(admin.ModelAdmin):
	list_display = ['id_attribute_group', 'is_color_group','name', 'public_name', 'group_type', 'position']
	inlines=[AttributeGroupShopInline,]

class AttributeGroupShopAdmin(admin.ModelAdmin):
	list_display = ['id_attribute_group','id_shop']

class AttributeAdmin(admin.ModelAdmin):
	list_display = ['id_attribute', 'id_attribute_group','name', 'color','position']
	inlines=[AttributeShopInline,]

class AttributeShopAdmin(admin.ModelAdmin):
	list_display = ['id_attribute','id_shop']

class ProductAttributeAdmin(admin.ModelAdmin):
	list_display = ['id_product_attribute', 'id_product','reference','ean13','upc','wholesale_price','price','quantity','weight','unit_price_impact','default_on', 'minimal_quantity','available_date']
	inlines=[ProductAttributeCombinationInline,ProductAttributeShopInline, ]

class ProductAttributeCombinationAdmin(admin.ModelAdmin):
	list_display = ['id_attribute', 'id_product_attribute']

class ProductAttributeShopAdmin(admin.ModelAdmin):
	list_display = ['id_product_attribute', 'id_shop','wholesale_price','price','weight','unit_price_impact','default_on','minimal_quantity', 'available_date']

class ProductAdmin(admin.ModelAdmin):
	list_display = ['id_product', 'id_category_default','id_shop_default','name','description','on_sale','online_only', 'quantity', 'price']

class CategoryProductAdmin(admin.ModelAdmin):
	list_display = ['id_category','id_product','position']

class AttributeImpactAdmin(admin.ModelAdmin):
	list_display = ['id_attribute_impact', 'id_product','id_attribute','weight','price']

class ImageAdmin(admin.ModelAdmin):
	list_display = ['id_image','id_product','image','legend','position','cover']
	inlines = [ProductAttributeImageInline,]

class ProductAttributeImageAdmin(admin.ModelAdmin):
	list_display = ['id_product_attribute','id_image']

class ProductShopAdmin(admin.ModelAdmin):
	list_display = ['id_product', 'id_shop', 'id_category_default','on_sale','online_only','price']


# Tiendas
admin.site.register(Shop, ShopAdmin)
admin.site.register(ShopGroup, ShopGroupAdmin)
admin.site.register(CategoryShop, CategoryShopAdmin)

# Grupos
admin.site.register(Groups, GroupsAdmin)
admin.site.register(CategoryGroup, CategoryGroupAdmin)

#Categorias
admin.site.register(Category, CategoryAdmin)

# Grupos de atributos 
admin.site.register(AttributeGroup, AttributeGroupAdmin)
admin.site.register(AttributeGroupShop, AttributeGroupShopAdmin)

# Atributos
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(AttributeShop, AttributeShopAdmin)

# Atributos de los productos
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(ProductAttributeCombination, ProductAttributeCombinationAdmin)
admin.site.register(ProductAttributeShop, ProductAttributeShopAdmin)

# Productos 
admin.site.register(Product, ProductAdmin)
admin.site.register(CategoryProduct, CategoryProductAdmin)
admin.site.register(AttributeImpact, AttributeImpactAdmin)

# Imagenes
admin.site.register(Image, ImageAdmin)
admin.site.register(ProductAttributeImage, ProductAttributeImageAdmin)

# Productos anidados 
admin.site.register(ProductShop, ProductShopAdmin)

'''
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

'''