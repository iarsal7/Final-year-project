# Generated by Django 3.0.5 on 2020-04-18 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerce', '0004_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product',
            field=models.ManyToManyField(to='Ecommerce.Product'),
        ),
    ]
