# Generated by Django 2.1.7 on 2019-02-27 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_mailverification'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailverification',
            name='type',
            field=models.CharField(blank=True, choices=[('PASAPORTE', 'Pasaporte'), ('RUT', 'RUT'), ('CEDULA', 'Cedula')], max_length=20, verbose_name='Tipo de Transaccion'),
        ),
    ]
