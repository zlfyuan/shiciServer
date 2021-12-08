# Generated by Django 3.2.9 on 2021-12-08 17:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerifyRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4, verbose_name='验证码')),
                ('email', models.EmailField(max_length=50, verbose_name='邮箱')),
                ('send_type', models.CharField(choices=[('register', '注册'), ('login', '登录'), ('forget', '找回密码')], max_length=10, verbose_name='验证码类型')),
                ('send_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='发送时间')),
                ('send_status', models.BooleanField(default=False, verbose_name='是否发送成功,默认为False')),
                ('send_temp', models.CharField(default=None, max_length=100, verbose_name='内容模板')),
                ('send_title', models.CharField(default=None, max_length=100, verbose_name='验证标题')),
            ],
            options={
                'verbose_name': '2. 邮箱验证码',
                'verbose_name_plural': '2. 邮箱验证码',
                'ordering': ['-send_time'],
            },
        ),
    ]