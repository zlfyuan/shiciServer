# Generated by Django 3.2.9 on 2021-11-19 18:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gushi', '0006_auto_20211119_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='gushipinyins',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='创建时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gushipinyins',
            name='last_change_date',
            field=models.DateTimeField(auto_now=True, verbose_name='最后修改日期'),
        ),
    ]