# Generated by Django 2.2.3 on 2020-03-08 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_soldproduct_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultantacceptsoldproductrequest',
            name='sold_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.SoldProduct'),
        ),
    ]
