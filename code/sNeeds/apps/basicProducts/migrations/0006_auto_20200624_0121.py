# Generated by Django 2.2.3 on 2020-06-23 20:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basicProducts', '0005_auto_20200618_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroomlink',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basicproducts_classroomlink', to='basicProducts.ClassProduct'),
        ),
        migrations.AlterField(
            model_name='classwebinar',
            name='holding_date_times',
            field=models.ManyToManyField(related_name='basicproducts_classwebinar', to='basicProducts.HoldingDateTime'),
        ),
        migrations.AlterField(
            model_name='classwebinar',
            name='lecturers_short',
            field=models.ManyToManyField(related_name='basicproducts_classwebinar', to='basicProducts.Lecturer'),
        ),
        migrations.AlterField(
            model_name='classwebinar',
            name='question_answers',
            field=models.ManyToManyField(related_name='basicproducts_classwebinar', to='basicProducts.QuestionAnswer'),
        ),
        migrations.AlterField(
            model_name='roomlink',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='webinarroomlink',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basicproducts_webinarroomlink', to='basicProducts.WebinarProduct'),
        ),
    ]
