# Generated by Django 2.1.7 on 2019-03-18 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
        ('products', '0003_auto_20190318_1733'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shop',
            unique_together={('url', 'customer')},
        ),
    ]