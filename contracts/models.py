from django.db import models
from customers.models import *
from services.models import Service

# Create your models here.


class Contracts(models.Model):
    STATE_CONTRACT = (
        ('ORDEN', 'ORDEN'),
        ('PAYMENT', 'PAGADO'),
        ('DELETE', 'ELIMINADO'),
    )
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    #services = models.ManyToManyField(ServiceContract)
    date_contract = models.DateField(verbose_name="Fecha del Contrato")
    total = models.FloatField()
    state = models.CharField(verbose_name="Estado del Contrato",max_length=20,choices=STATE_CONTRACT)
    def __str__(self):
        return self.customer.alias

class ServiceContract(models.Model):
    contract = models.ForeignKey(Contracts,on_delete=models.CASCADE,blank=True)
    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    date_init = models.DateField(verbose_name="Fecha de Inicio")
    date_end = models.DateField(verbose_name="Fecha de Finalizacion")
    quantity = models.IntegerField(default=1)
    amount = models.FloatField()
    tax = models.FloatField()
    total = models.FloatField()
    def __str__(self):
        return self.service.name


class Payment(models.Model):
    TYPE_PAYMENT =(
        ('TRANSFERENCE','Transferencia'),
        ('BTC','Transferencia'),
        ('TDC','Tarjeta de Credito'),
    )
    STATUS_PAYMENT =(
        ('APPROVED','Aprobado'),
        ('REJECTED','Rechazado'),
        ('PENDING','Pendiente'),
    )
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    type = models.CharField(verbose_name="Tipo de Pago",max_length=20,choices=TYPE_PAYMENT)
    reference = models.CharField(verbose_name="Referencia",max_length=200)
    amount = models.FloatField()
    date_payment = models.DateTimeField(verbose_name="Fecha y Hora del Pago")


class InvoiceContract(models.Model):
    number = models.IntegerField(default=1)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    contract = models.ForeignKey(Contracts,on_delete=models.CASCADE)
    payment = models.ManyToManyField(Payment)
    date_invoice = models.DateField(verbose_name="Fecha de la Factura")
    address_invoice = models.ForeignKey(AddressCustomer,verbose_name="Direccion de Facturacion",on_delete=models.CASCADE,related_name="address_invoice")
    address_delivery = models.ForeignKey(AddressCustomer,verbose_name="Direccion de Entrega",on_delete=models.CASCADE,related_name="address_delivery")
    amount = models.FloatField()
    tax = models.FloatField()
    total = models.FloatField()
