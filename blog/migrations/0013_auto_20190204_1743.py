# Generated by Django 2.1.3 on 2019-02-04 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20190204_1546'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=120)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.CharField(blank=True, help_text='Sample form : آریا، آمریکا، اپلای', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='usercomment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.Post'),
        ),
    ]
