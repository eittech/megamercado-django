# Generated by Django 2.1.7 on 2019-02-18 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_categorytags'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('shop', 'name')},
        ),
    ]
