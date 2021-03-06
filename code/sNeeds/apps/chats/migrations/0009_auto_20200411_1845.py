# Generated by Django 2.2.3 on 2020-04-11 14:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0008_auto_20200308_0809'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chat',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
