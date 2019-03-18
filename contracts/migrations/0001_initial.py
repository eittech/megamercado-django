# Generated by Django 2.1.7 on 2019-03-18 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('services', '0001_initial'),
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contracts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_contract', models.DateField(verbose_name='Fecha del Contrato')),
                ('total', models.FloatField()),
                ('state', models.CharField(choices=[('ORDEN', 'ORDEN'), ('PAYMENT', 'PAGADO'), ('DELETE', 'ELIMINADO')], max_length=20, verbose_name='Estado del Contrato')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=1)),
                ('date_invoice', models.DateField(verbose_name='Fecha de la Factura')),
                ('amount', models.FloatField()),
                ('tax', models.FloatField()),
                ('total', models.FloatField()),
                ('address_delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address_delivery', to='customers.AddressCustomer', verbose_name='Direccion de Entrega')),
                ('address_invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address_invoice', to='customers.AddressCustomer', verbose_name='Direccion de Facturacion')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.Contracts')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('TRANSFERENCE', 'Transferencia'), ('BTC', 'Transferencia'), ('TDC', 'Tarjeta de Credito')], max_length=20, verbose_name='Tipo de Pago')),
                ('reference', models.CharField(max_length=200, verbose_name='Referencia')),
                ('amount', models.FloatField()),
                ('date_payment', models.DateTimeField(verbose_name='Fecha y Hora del Pago')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_init', models.DateField(verbose_name='Fecha de Inicio')),
                ('date_end', models.DateField(verbose_name='Fecha de Finalizacion')),
                ('quantity', models.IntegerField(default=1)),
                ('amount', models.FloatField()),
                ('tax', models.FloatField()),
                ('total', models.FloatField()),
                ('contract', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='contracts.Contracts')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.Service')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceContractProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('servicecontract', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='contracts.ServiceContract')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceContractShop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servicecontract', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='contracts.ServiceContract')),
                ('shop', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='products.Shop')),
            ],
        ),
        migrations.AddField(
            model_name='invoicecontract',
            name='payment',
            field=models.ManyToManyField(to='contracts.Payment'),
        ),
    ]
