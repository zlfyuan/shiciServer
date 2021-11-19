# Generated by Django 3.2.9 on 2021-11-19 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gushi', '0004_rename_tag_songci_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tangshisanbai',
            old_name='TangShi_ptr',
            new_name='tangshi_ptr',
        ),
        migrations.AddField(
            model_name='songci',
            name='author_pinyin',
            field=models.CharField(max_length=300, null=True, verbose_name='宋词作者_pinyin'),
        ),
        migrations.AddField(
            model_name='songci',
            name='paragraphs_pinyin',
            field=models.TextField(max_length=5000, null=True, verbose_name='宋词内容_pinyin'),
        ),
        migrations.AddField(
            model_name='songci',
            name='title_pinyin',
            field=models.CharField(max_length=300, null=True, verbose_name='宋词标题_pinyin'),
        ),
        migrations.AddField(
            model_name='tangshi',
            name='author_pinyin',
            field=models.CharField(max_length=300, null=True, verbose_name='古诗作者_pinyin'),
        ),
        migrations.AddField(
            model_name='tangshi',
            name='paragraphs_pinyin',
            field=models.TextField(max_length=5000, null=True, verbose_name='古诗内容_pinyin'),
        ),
        migrations.AddField(
            model_name='tangshi',
            name='title_pinyin',
            field=models.CharField(max_length=300, null=True, verbose_name='古诗标题_pinyin'),
        ),
    ]
