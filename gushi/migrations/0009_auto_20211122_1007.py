# Generated by Django 3.2.9 on 2021-11-22 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gushi', '0008_auto_20211119_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='songci',
            name='strains',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='gushi.strains', verbose_name='节奏'),
        ),
        migrations.AddField(
            model_name='tangshi',
            name='strains',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='gushi.strains', verbose_name='节奏'),
        ),
    ]