# Generated by Django 2.2.3 on 2020-02-21 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_soldproduct_created'),
        ('orders', '0002_remove_order_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(blank=True, to='store.SoldProduct'),
        ),
    ]
