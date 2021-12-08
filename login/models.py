from django.db import models
from django.utils import timezone
import datetime


# 邮箱验证
class EmailVerifyRecord(models.Model):
    # 验证码
    code = models.CharField(max_length=4, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    # 包含注册验证和找回验证
    send_type = models.CharField(verbose_name="验证码类型", max_length=10,
                                 choices=(("register", "注册"), ("login", "登录"), ("forget", "找回密码")))
    send_time = models.DateTimeField(verbose_name="发送时间", default=timezone.now)
    send_status = models.BooleanField(verbose_name="是否发送成功,默认为False", default=False)
    send_temp = models.CharField(verbose_name="内容模板", max_length=100, default=None)
    send_title = models.CharField(verbose_name="验证标题", max_length=100, default=None)

    class Meta:
        ordering = ["-send_time"]
        verbose_name = u"2. 邮箱验证码"
        verbose_name_plural = verbose_name

    def is_invalid(self):
        print(self.send_time)
        print(timezone.now() - datetime.timedelta(minutes=2))
        return self.send_time < timezone.now() - datetime.timedelta(minutes=2)

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)
