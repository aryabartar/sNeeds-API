# Generated by Django 2.2.3 on 2020-02-21 13:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20200221_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='time_slot_sales_number_discount',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
            preserve_default=False,
        ),
    ]
