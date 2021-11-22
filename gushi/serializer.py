from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Author, TangShi, GuShiPinYins, SongCi


class GuShiPinYinsSeriliazer(ModelSerializer):
    class Meta:
        model = GuShiPinYins
        fields = '__all__'


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class TangShiSerializer(ModelSerializer):

    # pinyin = serializers.SerializerMethodField()
    #
    # def get_pinyin(self, obj):
    #     print(type(obj.pinyin))
    #     print(obj.pinyin)
    #     label = obj.pinyin
    #     l = GuShiPinYinsSeriliazer(label, many=True)
    #     return l.data

    class Meta:
        model = TangShi
        fields = '__all__'


class SongCiSerializer(ModelSerializer):

    class Meta:
        model = SongCi
        fields = '__all__'
