# Generated by Django 2.2.3 on 2020-03-12 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Webinar',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.Product')),
                ('title', models.CharField(max_length=256)),
                ('slug', models.SlugField(unique=True)),
                ('active', models.BooleanField(default=True)),
            ],
            bases=('store.product',),
        ),
        migrations.CreateModel(
            name='SoldWebinar',
            fields=[
                ('soldproduct_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.SoldProduct')),
                ('webinar', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='webinars.Webinar')),
            ],
            bases=('store.soldproduct',),
        ),
    ]
