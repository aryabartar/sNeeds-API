# Generated by Django 2.2.3 on 2019-09-12 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discounts', '0011_auto_20190811_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslotsalenumberdiscount',
            name='number',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]
