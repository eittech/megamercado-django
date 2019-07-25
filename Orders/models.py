from django.db import models
from customers.models import Customer
from products.models import *
from carrier.models import *
from currency.models import *
from locations.models import *
from django.core.validators import MinValueValidator

# Create your models here.

#CARRITO 

class Cart(models.Model):
    id_cart = models.AutoField(primary_key=True)
    delivery_option = models.TextField()
    id_customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_add = models.DateTimeField()
    date_upd = models.DateTimeField()
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_cart)

class CartRule(models.Model):
    id_cart_rule = models.AutoField(primary_key=True)
    id_customer =  models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    name = models.CharField(max_length=254, blank=False)
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    quantity_per_user = models.IntegerField(validators=[MinValueValidator(0)])
    priority = models.IntegerField()
    code = models.CharField(max_length=254) # Codigo que se uso en el pago
    minimum_amount = models.DecimalField(max_digits=17, decimal_places=2)
    minimum_amount_tax = models.IntegerField(validators=[MinValueValidator(0)])
    minimum_amount_currency = models.IntegerField(validators=[MinValueValidator(0)])
    minimum_amount_shipping = models.IntegerField(validators=[MinValueValidator(0)])
    country_restriction = models.BooleanField(blank=True, default=False)
    carrier_restriction = models.BooleanField(blank=True, default=False)
    group_restriction = models.BooleanField(blank=True, default=False)
    cart_rule_restriction = models.BooleanField(blank=True, default=False)
    product_restriction = models.BooleanField(blank=True, default=False)
    shop_restriction = models.BooleanField(blank=True, default=False)
    free_shipping = models.BooleanField(blank=True, default=False)
    reduction_percent = models.DecimalField(max_digits=5, decimal_places=2)
    reduction_amount = models.DecimalField(max_digits=17, decimal_places=2)
    reduction_tax = models.IntegerField(validators=[MinValueValidator(0)])
    reduction_currency = models.IntegerField(validators=[MinValueValidator(0)])
    reduction_product = models.IntegerField(validators=[MinValueValidator(0)])
    gift_product = models.IntegerField()
    gift_product_attribute = models.IntegerField()
    active = models.BooleanField(blank=True, default=False)
    date_add = models.DateTimeField()
    date_upd = models.DateTimeField()
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.name)

class CartCartRule(models.Model):
    id_cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    id_cart_rule = models.ForeignKey(CartRule, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('id_cart', 'id_cart_rule'),)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_cart) +" "+ str(self.id_cart_rule) 

class CartProduct(models.Model):
    id_cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    id_product_attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    date_add = models.DateTimeField()
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_cart) + " "+ str(self.id_product)

class CartRuleCountry(models.Model):
    id_cart_rule = models.ForeignKey(CartRule, on_delete=models.CASCADE)
    id_country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('id_cart_rule', 'id_country'),)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_cart_rule) +" "+ str(self.id_country)

class Orders(models.Model):
    id_order = models.AutoField(primary_key=True)
    reference = models.CharField(max_length=9, blank=True, null=True)
    id_customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    id_cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    id_shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    id_carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)
    id_address_delivery = models.ForeignKey(Address,related_name='delivery', on_delete=models.CASCADE)
    id_address_invoice = models.ForeignKey(Address, related_name='invoice',on_delete=models.CASCADE)
    id_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    current_state = models.IntegerField(blank=True, null=True)
    shipping_number = models.CharField(max_length=64, blank=True, null=True)
    shipping_date = models.DateField(blank=True, null=True)
    total_discounts = models.DecimalField(max_digits=17, decimal_places=2)
    total_paid = models.DecimalField(max_digits=17, decimal_places=2)
    total_paid_real = models.DecimalField(max_digits=17, decimal_places=2)
    total_products = models.DecimalField(max_digits=17, decimal_places=2)
    total_shipping = models.DecimalField(max_digits=17, decimal_places=2)
    delivery_date = models.DateTimeField(blank=True, null=True)
    valid = models.BooleanField(blank=True, default=False)
    date_add = models.DateTimeField()
    date_upd = models.DateTimeField()

    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_order)

class OrderCartRule(models.Model):
    id_order_cart_rule = models.AutoField(primary_key=True)
    id_order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    id_cart_rule = models.ForeignKey(CartRule, on_delete=models.CASCADE)
    name = models.CharField(max_length=254)
    value = models.DecimalField(max_digits=17, decimal_places=2)
    value_tax_excl = models.DecimalField(max_digits=17, decimal_places=2)
    free_shipping = models.BooleanField(blank=True, default=False)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_order_cart_rule)

class OrderInvoice(models.Model):
    id_order_invoice = models.AutoField(primary_key=True)
    id_order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    number = models.IntegerField()
    delivery_number = models.IntegerField()
    delivery_date = models.DateTimeField(blank=True, null=True)
    total_discount_tax_excl = models.DecimalField(max_digits=17, decimal_places=2)
    total_discount_tax_incl = models.DecimalField(max_digits=17, decimal_places=2)
    total_paid_tax_excl = models.DecimalField(max_digits=17, decimal_places=2)
    total_paid_tax_incl = models.DecimalField(max_digits=17, decimal_places=2)
    total_products = models.DecimalField(max_digits=17, decimal_places=2)
    total_products_wt = models.DecimalField(max_digits=17, decimal_places=2)
    total_shipping_tax_excl = models.DecimalField(max_digits=17, decimal_places=2)
    total_shipping_tax_incl = models.DecimalField(max_digits=17, decimal_places=2)
    shipping_tax_computation_method = models.IntegerField()
    total_wrapping_tax_excl = models.DecimalField(max_digits=17, decimal_places=2)
    total_wrapping_tax_incl = models.DecimalField(max_digits=17, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    date_add = models.DateTimeField()
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_order_invoice)

class OrderDetail(models.Model):
    id_order_detail = models.AutoField(primary_key=True)
    id_order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_attribute_id =  models.CharField(max_length=200, blank=True, null=True)
    product_name = models.CharField(max_length=255)
    product_quantity = models.IntegerField(validators=[MinValueValidator(0)])
    product_price = models.DecimalField(max_digits=20, decimal_places=6)
    product_ean13 = models.CharField(max_length=13, blank=True, null=True)
    product_upc = models.CharField(max_length=12, blank=True, null=True)
    product_reference = models.CharField(max_length=32, blank=True, null=True)
    product_weight = models.DecimalField(max_digits=20, decimal_places=6)
    purchase_supplier_price = models.DecimalField(max_digits=20, decimal_places=6)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_order_detail)

class Tax(models.Model):
    id_tax = models.AutoField(primary_key=True)
    rate = models.DecimalField(max_digits=10, decimal_places=3)
    active = models.BooleanField(blank=True, default=False)
    deleted = models.BooleanField(blank=True, default=False)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_tax)

class OrderDetailTax(models.Model):
    id_order_detail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE)
    id_tax = models.ForeignKey(Tax, on_delete=models.CASCADE)
    unit_amount = models.DecimalField(max_digits=16, decimal_places=6)
    total_amount = models.DecimalField(max_digits=16, decimal_places=6)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_order_detail) +" "+ str(self.id_tax)

class OrderState(models.Model):
    id_order_state = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    template = models.CharField(max_length=64)
    invoice = models.BooleanField(blank=True, default=False)
    send_email = models.BooleanField(blank=True, default=False)
    unremovable = models.BooleanField(blank=True, default=False)
    hidden = models.BooleanField(blank=True, default=False)
    logable = models.BooleanField(blank=True, default=False)
    delivery = models.BooleanField(blank=True, default=False)
    shipped = models.BooleanField(blank=True, default=False)
    paid = models.BooleanField(blank=True, default=False)
    deleted = models.BooleanField(blank=True, default=False)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_order_state)

class OrderHistory(models.Model):
    id_order_history = models.AutoField(primary_key=True)
    id_order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    id_order_state = models.ForeignKey(OrderState, on_delete=models.CASCADE)
    date_add = models.DateTimeField()
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_order_history)


class OrderInvoiceTax(models.Model):
    id_order_invoice = models.ForeignKey(OrderInvoice, on_delete=models.CASCADE)
    type = models.CharField(max_length=15)
    id_tax = models.ForeignKey(Tax, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=6)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_order_invoice)

class OrderMessage(models.Model):
    id_order_message = models.AutoField(primary_key=True)
    id_customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, blank=False)
    message = models.TextField()
    date_add = models.DateTimeField()
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.name)

class OrderOrderMessage(models.Model):
    id_order_message = models.ForeignKey(OrderMessage, on_delete=models.CASCADE)
    id_order = models.ForeignKey(Orders, on_delete=models.CASCADE)

    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id)


