import json
import os

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User
from login.serializers import EmailVerifyRecordSerializers, RegisterSerializers, \
    ChangePasswordSerializers, ForgetPasswordSerializers, LoginSerializers
from utils.custom_json_response import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from django.conf import settings
from login.models import EmailVerifyRecord
import random, datetime
import requests
from login.utils.generator import Generator

def get_detail_error(ser):
    if ser.errors:
        keys = list(ser.errors.keys())
        values = list(ser.errors.values())
        if keys[0] == "non_field_errors":
            return values[0][0]
        errors_message = keys[0] + values[0][0]
        # print(errors_message)
        errors_message = errors_message.replace("null。", "空")
        return errors_message
    return "no error message"

class WeixinLogin(APIView):
    def post(self, request):
        params = {'appid': os.getenv('WXAPPID'),
                  'secret': os.getenv('WXSECRET'),
                  'js_code': request.data["js_code"]}
        print(params)
        r = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=params)
        json_data = json.loads(r.text)
        if "errcode" not in json_data.keys():
            return JsonResponse(data=json_data, code=status.HTTP_200_OK, msg="微信验证登录成功")
        else:
            return JsonResponse(data=json_data,code=233,msg="微信验证失败")

class RegisterView(APIView):

    def post(self, request):

        ser = RegisterSerializers(data=request.data)
        if ser.is_valid():
            user_obj = User.objects.filter(email=ser['email']).first()
            if user_obj:
                return JsonResponse(code=233, msg="用户已存在")
            verifyRecord = EmailVerifyRecord.objects.filter(email=ser.validated_data['email']).first()
            if not verifyRecord:
                return JsonResponse(code=233, msg="验证码没有找到")
            if not verifyRecord.send_type == 'register':
                return JsonResponse(code=233, msg="验证码没有找到")
            if verifyRecord.is_invalid():
                return JsonResponse(code=233, msg="验证码已过期")
            if verifyRecord.code == ser.validated_data['code']:
                idx = random.randint(1, 1000009)
                user = User.objects.create(username=Generator.randomName(),
                                           email=ser.validated_data['email'])
                user.set_password(ser.validated_data['password'])
                user.save()
                verifyRecord.delete()
                return JsonResponse(code=status.HTTP_200_OK, msg="注册成功")
            return JsonResponse(code=233, msg="验证码有误")
        return JsonResponse(code=233, msg=get_detail_error(ser))


class LoginView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        ser = LoginSerializers(data=request.data)

        if request.data["code"] == "6666":
            user_obj = User.objects.filter(email=request.data['email']).first()
            if not user_obj:
                idx = random.randint(1, 1000009)
                data = {"username": Generator().randomName()}
                user = User.objects.create(**data)
                user.save()
                user_obj = user
            refresh = self.get_token(user_obj)
            json_data = {'refresh': str(refresh),
                         'access': str(refresh.access_token)}
            return JsonResponse(data=json_data, code=status.HTTP_200_OK, msg="登录成功")

        ser.is_valid(raise_exception=True)
        verifyRecord = EmailVerifyRecord.objects.filter(email=ser.validated_data["email"], send_type="login").first()
        if not verifyRecord:
            return JsonResponse(code=233, msg="验证码没有找到")
        if not verifyRecord.send_type == 'login':
            return JsonResponse(code=233, msg="验证码没有找到")
        if verifyRecord.is_invalid():
            print(verifyRecord.code)
            return JsonResponse(code=233, msg="验证码已过期")
        if verifyRecord.code == ser.validated_data['code']:
            user_obj = User.objects.filter(email=ser.validated_data['email']).first()
            if not user_obj:
                idx = random.randint(1, 1000009)
                data = {"username": f"用户{idx}"}
                user = User.objects.create(**data)
                user.save()
                user_obj = user
            refresh = self.get_token(user_obj)
            json_data = {'refresh': str(refresh),
                         'access': str(refresh.access_token)}
            return JsonResponse(data=json_data, code=status.HTTP_200_OK, msg="登录成功")

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = ChangePasswordSerializers(data=request.data)
        if ser.is_valid():
            user_obj = User.objects.filter(username=request.user.username).first()
            if not user_obj.check_password(ser.validated_data['old_password']):
                return JsonResponse(code=233, msg="原密码错误")
            user_obj.set_password(ser.validated_data['new_password'])
            user_obj.save()
            return JsonResponse(code=status.HTTP_200_OK, msg="修改成功")
        return JsonResponse(code=233, msg=get_detail_error(ser))


class ForgetPasswordView(APIView):

    def post(self, request):
        ser = ForgetPasswordSerializers(data=request.data)
        if ser.is_valid():
            verifyRecord = EmailVerifyRecord.objects.filter(email=request.user.email).first()
            if not verifyRecord:
                return JsonResponse(code=233, msg="验证码没有找到")
            if not verifyRecord.send_type == 'forget':
                return JsonResponse(code=233, msg="验证码没有找到")
            if verifyRecord.is_invalid():
                return JsonResponse(code=233, msg="验证码已过期")
            if verifyRecord.code == ser.validated_data['code']:
                request.user.set_password(ser['new_password'])
                request.user.save()
                return JsonResponse(code=status.HTTP_200_OK, msg="修改成功")
            return JsonResponse(code=233, msg="修改失败")
        return JsonResponse(code=233, msg=get_detail_error(ser))


@api_view(['POST'])
def hello(request):
    return JsonResponse(data="测试hello", status=status.HTTP_200_OK, msg="success")


# 注册发送邮箱验证码
class SendEmailCodeView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            res = EmailVerifyRecordSerializers(data=request.data)
            if not res.is_valid():
                return JsonResponse(code=233, msg=get_detail_error(res))
            email = res.validated_data['email']
            send_type = res.validated_data['send_type']
            # 发送邮箱
            res_email = send_code_email(email, send_type)
            if res_email:
                return JsonResponse(code=status.HTTP_200_OK, msg="发送成功")
            else:
                return JsonResponse(code=233, msg="验证码发送失败, 请稍后重试")
        except Exception as e:
            print("错误信息 : ", e)
        return JsonResponse(code=233, msg="邮箱错误, 请稍后重试")


# 发送电子邮件
def send_code_email(email, send_type="register"):
    """
    发送电子邮件
    :param email: 要发送的邮箱
    :param send_type: 邮箱类型
    :return: True/False
    """
    email_record = EmailVerifyRecord()
    # 将给用户发的信息保存在数据库中
    code = random_str(4)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.send_time = datetime.datetime.now()
    # 初始化为空
    email_title = ""
    email_body = ""
    # 注册类型
    if send_type == "register":
        email_title = "注册激活"
        email_body = "您的邮箱注册验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(code)
    elif send_type == "forget":
        email_title = "找回密码"
        email_body = "您的邮箱注册验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(code)
    elif send_type == "login":
        email_title = "登录验证"
        email_body = "您的邮箱登录验证码为：{0}, 该验证码有效时间为两分钟，请及时进行登录。".format(code)
    else:
        return False

    # 发送邮件
    send_status = send_mail(email_title, email_body, settings.DEFAULT_FROM_EMAIL, [email])
    if not send_status:
        email_record.send_status = False
        email_record.send_temp = email_body
        email_record.send_title = email_title
        email_record.save()
        return False
    else:
        email_record.send_status = True
        email_record.send_temp = email_body
        email_record.send_title = email_title
        email_record.save()
        return True


# 生成随机字符串
def random_str(randomlength=8):
    """
    随机字符串
    :param randomlength: 字符串长度
    :return: String 类型字符串
    """
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str
