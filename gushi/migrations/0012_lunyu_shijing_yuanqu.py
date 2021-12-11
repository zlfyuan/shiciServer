# Generated by Django 3.2.9 on 2021-12-11 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gushi', '0011_auto_20211122_1400'),
    ]

    operations = [
        migrations.CreateModel(
            name='YuanQu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=300, verbose_name='元曲作者')),
                ('title', models.CharField(max_length=300, verbose_name='元曲标题')),
                ('poet_id', models.CharField(max_length=100, null=True, verbose_name='元曲原始_ id')),
                ('paragraphs', models.TextField(max_length=5000, verbose_name='元曲内容')),
                ('dynasty', models.CharField(max_length=100, verbose_name='元曲原始_ id')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('last_change_date', models.DateTimeField(auto_now=True, verbose_name='最后修改日期')),
                ('tags', models.CharField(max_length=300, null=True, verbose_name='元曲tag')),
                ('author_id', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='gushi.author', verbose_name='作者')),
                ('pinyin', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='gushi.gushipinyins', verbose_name='拼音')),
                ('strains', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='gushi.strains', verbose_name='节奏')),
            ],
            options={
                'verbose_name': '元曲',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ShiJing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=300, verbose_name='诗经作者')),
                ('title', models.CharField(max_length=300, verbose_name='诗经标题')),
                ('poet_id', models.CharField(max_length=100, null=True, verbose_name='诗经原始_ id')),
                ('paragraphs', models.TextField(max_length=5000, verbose_name='诗经内容')),
                ('dynasty', models.CharField(max_length=100, verbose_name='诗经')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('last_change_date', models.DateTimeField(auto_now=True, verbose_name='最后修改日期')),
                ('tags', models.CharField(max_length=300, null=True, verbose_name='诗经tag')),
                ('author_id', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='gushi.author', verbose_name='作者')),
                ('pinyin', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='gushi.gushipinyins', verbose_name='拼音')),
                ('strains', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='gushi.strains', verbose_name='节奏')),
            ],
        ),
        migrations.CreateModel(
            name='LunYu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=300, verbose_name='论语作者')),
                ('title', models.CharField(max_length=300, verbose_name='论语标题')),
                ('poet_id', models.CharField(max_length=100, null=True, verbose_name='论语原始_ id')),
                ('paragraphs', models.TextField(max_length=5000, verbose_name='论语内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('last_change_date', models.DateTimeField(auto_now=True, verbose_name='最后修改日期')),
                ('tags', models.CharField(max_length=300, null=True, verbose_name='论语tag')),
                ('author_id', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='gushi.author', verbose_name='作者')),
                ('pinyin', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='gushi.gushipinyins', verbose_name='拼音')),
                ('strains', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='gushi.strains', verbose_name='节奏')),
            ],
        ),
    ]