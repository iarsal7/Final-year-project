# Generated by Django 3.0.5 on 2020-05-23 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerce', '0002_orderdetail_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]