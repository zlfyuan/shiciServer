from rest_framework import serializers
from user.models import User
from .models import EmailVerifyRecord
from rest_framework_simplejwt.serializers import RefreshToken
import random


class RegisterSerializers(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=16)
    password1 = serializers.CharField(max_length=16)
    code = serializers.CharField(max_length=4)

    class Meta:
        model = User
        fields = ('email', 'password', 'password1', 'code')

    def validate(self, attrs):
        data = attrs
        if data['password'] != data['password1']:
            raise serializers.ValidationError("两次密码不一致")
        return data


class ChangePasswordSerializers(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length=16)
    new_password = serializers.CharField(max_length=16)
    new_comfi_password = serializers.CharField(max_length=16)

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'new_comfi_password')

    def validate(self, attrs):
        data = super().validate(attrs)
        if data['new_comfi_password'] != data['new_password']:
            raise serializers.ValidationError("两次新密码不一致")
        return data


class ForgetPasswordSerializers(serializers.ModelSerializer):
    code = serializers.CharField(max_length=4)
    new_password = serializers.CharField(max_length=16)
    new_comfi_password = serializers.CharField(max_length=16)

    class Meta:
        model = User
        fields = ('code', 'new_password', 'new_comfi_password')

    def validate(self, attrs):
        data = super().validate(attrs)
        if data['new_comfi_password'] != data['new_password']:
            raise serializers.ValidationError("两次新密码不一致")
        return data


class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=4)

    def create(self, validated_data):
        return LoginSerializers(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.code = validated_data.get('code', instance.code)
        return instance


class EmailVerifyRecordSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmailVerifyRecord
        fields = ('email', 'send_type')
