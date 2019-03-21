from django.contrib import admin
from products.models import *
# Register your models here.
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAttributesInline(admin.TabularInline):
    model = ProductAttributes
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_filter = ('shop', 'category')
    list_display = ('name', 'price','tax','total')
    search_fields = ['name']
    inlines = (ProductAttributesInline,ProductImageInline)


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
    list_display = ('name', 'num_products',)


admin.site.register(Shop,ShopAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Attributes)
admin.site.register(ProductAttributes)
admin.site.register(FavoriteProduct)
