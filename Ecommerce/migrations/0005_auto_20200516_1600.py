# Generated by Django 3.0.5 on 2020-05-16 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerce', '0004_cart_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemvariation',
            name='variation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemvariations', to='Ecommerce.Variation'),
        ),
    ]