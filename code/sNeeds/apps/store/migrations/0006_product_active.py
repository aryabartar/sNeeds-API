# Generated by Django 2.2.3 on 2020-03-22 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20200308_0756'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
