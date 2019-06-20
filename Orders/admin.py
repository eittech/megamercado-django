from django.contrib import admin
from Orders.models import *

# Register your models here.

class CartProductInline(admin.TabularInline):
    model = CartProduct
    extra = 1

class CartCartRuleInline(admin.TabularInline):
    model = CartCartRule
    extra = 1

class CartRuleCountryInline(admin.TabularInline):
    model = CartRuleCountry
    extra = 1

class OrderCartRuleInline(admin.TabularInline):
    model = OrderCartRule
    extra = 1

class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 1

class OrderDetailTaxInline(admin.TabularInline):
    model = OrderDetailTax
    extra = 1

class OrderInvoiceTaxInline(admin.TabularInline):
    model = OrderInvoiceTax
    extra = 1

class OrderHistoryInline(admin.TabularInline):
    model = OrderHistory
    extra = 1

class OrderOrderMessageInline(admin.TabularInline):
    model = OrderOrderMessage
    extra = 1

class CartAdmin(admin.ModelAdmin):
    list_display = ['id_cart','delivery_option','id_customer','gift','gift_message']
    inlines=[CartProductInline,]

class CartProductAdmin(admin.ModelAdmin):
    list_display = ['id_cart','id_product','id_product_attribute','quantity','date_add']

class CartRuleAdmin(admin.ModelAdmin):
    list_display = ['id_cart_rule' ,'id_customer','date_from','date_to','name','description','quantity','quantity_per_user','code']
    inlines=[CartCartRuleInline,CartRuleCountryInline,]

class CartCartRuleAdmin(admin.ModelAdmin):
    list_display = ['id_cart','id_cart_rule']

class CartRuleCountryAdmin(admin.ModelAdmin):
    list_display = ['id_cart_rule', 'id_country']

class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id_order','reference','id_customer','id_cart','id_address_delivery','id_address_invoice','shipping_number','total_discounts', 'total_paid', 'total_products']
    inlines=[OrderCartRuleInline,]

class OrderCartRuleAdmin(admin.ModelAdmin):
    list_display = ['id_order_cart_rule', 'id_order','id_cart_rule','name','value','value_tax_excl','free_shipping']

class OrderInvoiceAdmin(admin.ModelAdmin):
    list_display = ['id_order_invoice','id_order','number','delivery_number','delivery_date','total_discount_tax_excl','total_discount_tax_incl','total_paid_tax_excl','total_paid_tax_incl', 'total_products']
    inlines=[OrderDetailInline,]

class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['id_order_detail', 'id_order', 'id_order_invoice', 'id_shop', 'product_id', 'product_attribute_id', 'product_name', 'product_quantity', 'product_quantity_in_stock','product_quantity_refunded']

class TaxAdmin(admin.ModelAdmin):
    list_display = ['id_tax','rate', 'active', 'deleted']
    inlines=[OrderDetailTaxInline,OrderInvoiceTaxInline,]

class OrderDetailTaxAdmin(admin.ModelAdmin):
    list_display = ['id_order_detail', 'id_tax','unit_amount','total_amount']

class OrderInvoiceTaxAdmin(admin.ModelAdmin):
    list_display = ['id_order_invoice','type','id_tax','amount']

class OrderStateAdmin(admin.ModelAdmin):
    list_display = ['id_order_state', 'name','template','invoice','send_email','unremovable','hidden','logable','delivery','shipped','paid', 'deleted']
    inlines=[OrderHistoryInline,]

class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ['id_order_history','id_order','id_order_state','date_add']

class OrderMessageAdmin(admin.ModelAdmin):
    list_display =['id_order_message','id_customer','name','message','date_add']
    inlines=[OrderOrderMessageInline,]

class OrderOrderMessageAdmin(admin.ModelAdmin):
    list_display = ['id_order_message','id_order']


#Carrito
admin.site.register(Cart, CartAdmin)
admin.site.register(CartProduct, CartProductAdmin)

# Reglas de carrito
admin.site.register(CartRule, CartRuleAdmin)
admin.site.register(CartCartRule,CartCartRuleAdmin)
admin.site.register(CartRuleCountry,CartRuleCountryAdmin)

# Ordenes
admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrderCartRule, OrderCartRuleAdmin)

# Factura
admin.site.register(OrderInvoice,OrderInvoiceAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)

#Tax
admin.site.register(Tax,TaxAdmin)
admin.site.register(OrderDetailTax, OrderDetailTaxAdmin)
admin.site.register(OrderInvoiceTax, OrderInvoiceTaxAdmin)

#Estado
admin.site.register(OrderState, OrderStateAdmin)
admin.site.register(OrderHistory,OrderHistoryAdmin)

#Mensaje
admin.site.register(OrderMessage,OrderMessageAdmin)
admin.site.register(OrderOrderMessage,OrderOrderMessageAdmin)