# Generated by Django 3.0.5 on 2020-05-06 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerce', '0008_auto_20200506_0242'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant_key', models.IntegerField(blank=True, null=True)),
                ('product_key', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'unique_together': {('variant_key', 'product_key')},
            },
        ),
    ]