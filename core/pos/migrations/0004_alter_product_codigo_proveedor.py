# Generated by Django 3.2.2 on 2023-07-23 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0003_product_codigo_proveedor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='codigo_proveedor',
            field=models.CharField(max_length=50, verbose_name='Código de Proveedor'),
        ),
    ]