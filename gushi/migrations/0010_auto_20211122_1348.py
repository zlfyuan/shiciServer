# Generated by Django 3.2.9 on 2021-11-22 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gushi', '0009_auto_20211122_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='songci',
            name='author_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='gushi.author', verbose_name='作者'),
        ),
        migrations.AddField(
            model_name='tangshi',
            name='author_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='gushi.author', verbose_name='作者'),
        ),
    ]