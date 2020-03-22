# Generated by Django 2.2.3 on 2020-03-22 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storePackages', '0024_auto_20200319_2000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='soldstorepackage',
            name='sold_store_package_phases',
        ),
        migrations.AddField(
            model_name='soldstorepackagephase',
            name='consultant_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='soldstorepackagephase',
            name='sold_store_package',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sold_store_package_phases', to='storePackages.SoldStorePackage'),
        ),
        migrations.AddField(
            model_name='soldstorepackagephase',
            name='status',
            field=models.CharField(choices=[('not_started', 'شروع نشده'), ('pay_to_start', 'نیازمند پرداخت برای شروع'), ('in_progress', 'در حال انجام'), ('done', 'انجام شده')], default='not_started', max_length=128),
        ),
    ]