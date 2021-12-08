from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render

from utils.custom_json_response import JsonResponse
from .models import User, FeedBack
from rest_framework.views import APIView

from .serializers import UserSerializer, FeedBackSerializers


class UserInfoView(APIView):

    def get(self, request):
        current_user = User.objects.all().filter(id=request.user.id).first()
        data = UserSerializer(current_user).data
        return JsonResponse(data=data)


class FeedBackView(APIView):

    def post(self, request):
        ser = FeedBackSerializers(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.validated_data["user"] = self.request.user

        FeedBack.objects.create(**ser.validated_data)

        return JsonResponse(msg="非常感谢～,收到您的反馈")


def index(request):
    template = loader.get_template('shudong/index.html')
    return HttpResponse(template.render({}, request))
