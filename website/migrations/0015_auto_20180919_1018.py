# Generated by Django 2.0.5 on 2018-09-19 05:48

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_topic_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='slug',
            field=models.SlugField(default=uuid.uuid1, unique=True),
        ),
    ]
