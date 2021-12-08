from django.db import models
from django.contrib.auth.models import AbstractUser

from shiciServer import settings


class User(AbstractUser):
    name = models.CharField(max_length=100, verbose_name="昵称")
    age = models.IntegerField(default=0, verbose_name="年龄")


class FeedBack(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE,
                             verbose_name='用户')
    feedback_content = models.TextField(verbose_name="反馈内容")
    creat_time = models.DateTimeField(auto_now_add=True, verbose_name="反馈时间")

    class Meta:
        verbose_name = "反馈意见"
        ordering = ["-creat_time"]
