# Generated by Django 3.0.5 on 2020-05-14 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerce', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
