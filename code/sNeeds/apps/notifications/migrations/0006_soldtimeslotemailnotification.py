# Generated by Django 2.2.3 on 2020-07-13 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0005_auto_20200520_1145'),
    ]

    operations = [
        migrations.CreateModel(
            name='SoldTimeSlotEmailNotification',
            fields=[
                ('emailnotification_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='notifications.EmailNotification')),
                ('sold_time_slot_id', models.PositiveIntegerField()),
            ],
            bases=('notifications.emailnotification',),
        ),
    ]
