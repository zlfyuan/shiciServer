import json
import os
import time

import django_filters
from django.shortcuts import render

# Create your views here.
from pypinyin import pinyin
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from setuptools.namespaces import flatten
from zhconv import convert_for_mw

from .models import Author, TangShi, SongCi, TangShiSanBai, Strains, SongCiSanBai, GuShiPinYins
from .serializer import AuthorSerializer, TangShiSerializer
from .utils.custom_json_response import JsonResponse
from .utils.custom_pagination import LargeResultsSetPagination
from .utils.custom_viewset_base import CustomViewBase


class TangShiView(CustomViewBase):
    queryset = TangShi.objects.all().order_by('id')
    serializer_class = TangShiSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        queryset = self.filter_queryset(self.get_queryset().all()[0:20])
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data, code=200, msg="success")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        zh_cn_title = zh_ft_convert_zh_cn(instance.title)
        zh_cn_author = zh_ft_convert_zh_cn(instance.author)
        zh_cn_paragraphs = zh_ft_convert_zh_cn(instance.paragraphs)

        zh_cn_paragraphs = zh_cn_paragraphs.replace("\'", "\"")

        _t = TangShi.objects.get(poet_id=instance.poet_id)
        _t.author = zh_cn_author
        _t.title = zh_cn_title
        _t.paragraphs = zh_cn_paragraphs
        if _t.pinyin == None:
            _list = json.loads(zh_cn_paragraphs)
            pinyi_paragraphs = []
            for i in _list:
                _pinyi_paragraphs = pinyin_convert(i)
                pinyi_paragraphs += _pinyi_paragraphs
            instance = GuShiPinYins.objects.update_or_create(author_pinyin=pinyin_convert(zh_cn_author),
                                                             title_pinyin=pinyin_convert(zh_cn_title),
                                                             paragraphs_pinyin=pinyi_paragraphs)
            _t.pinyin = instance[0]

        _t.save()

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(data=serializer.data, code=200, msg="success")


def pinyin_convert(text):
    try:
        pinyi = pinyin(text)
        return list(flatten(pinyi))
    except:
        return None


def zh_ft_convert_zh_cn(text):
    try:
        janti = convert_for_mw(text, 'zh-cn')
        return janti
    except:
        return text


class SearchView(APIView):

    def get(self, request):
        search_type = request.GET.get('type')
        pagination_class = LargeResultsSetPagination()
        search_class = filters.SearchFilter()

        self.search_fields = [search_type]

        list = TangShi.objects.all().order_by('id')

        search_query = search_class.filter_queryset(request=request, queryset=list, view=self)

        page_query = pagination_class.paginate_queryset(queryset=search_query, request=request, view=self)

        result_serializer = TangShiSerializer(page_query, many=True)

        page_result = pagination_class.get_paginated_response(result_serializer.data)

        return page_result


class GushiView(APIView):
    # queryset = TangShi.objects.all().order_by("id")
    # serializer_class = TangShiSerializer
    # saveAuthor()
    def get(self, request):
        # saveAuthor()
        # save()
        # saveTangShisanbai()
        # saveTangShiStrains()
        # savesongci()
        # savesongciSanbai()
        return JsonResponse(code=233, msg="fail")


def check_json(f, _dir):
    if not f.endswith('.json'):
        return True

    filepath = os.path.join(_dir, f)
    print(filepath)
    with open(filepath) as file:
        print(file)
        type(file)
        try:
            content = json.loads(file.read())
            # print(content)
            return content
            # return True
            # return file.read()
        except:
            assert False, f"{filepath} 校验失败"


def saveAuthor():
    name = "name𤤺"
    # if "𤤺" in name:
    # name = name.replace("𤤺", "")
    print(name, 13910389123801830183)
    start_time = time.time()
    filePath = "authors.tang.json"
    print(filePath)
    list = check_json(filePath, "gushi/chinese-poetry/json")
    for i in range(1, len(list)):
        print(i)
        item = list[i]
        print(item)
        name = item["name"]
        desc = item["desc"]
        author_id = item["id"]
        try:
            if isinstance(name, str) or \
                    isinstance(desc, str) or \
                    isinstance(author_id, str):
                Author.objects.update_or_create(name=name,
                                                desc=desc,
                                                author_id=author_id,
                                                dynasty=1)
        except ValueError:
            print(ValueError)

    end_time = time.time()
    print("耗时: {:.2f}秒".format(end_time - start_time))


def save():
    start_time = time.time()
    for i in range(0, 57):
        filePath = "poet.tang.{}000.json".format(i)
        print(filePath)
        list = check_json(filePath, "gushi/chinese-poetry/json")
        for idx in range(0, len(list)):
            print(filePath, idx)
            item = list[idx]
            print(item)
            author = item["author"]
            title = item["title"]
            paragraphs = item["paragraphs"]
            id = item["id"]
            tags = None
            if 'tags' in item:
                tags = item["tags"]

            try:
                TangShi.objects.update_or_create(author=author,
                                                 title=title,
                                                 paragraphs=paragraphs,
                                                 poet_id=id,
                                                 tags=tags)
            except ValueError:
                print(ValueError)

    end_time = time.time()
    # 关闭数据库连接
    print("耗时: {:.2f}秒".format(end_time - start_time))


def saveTangShisanbai():
    start_time = time.time()
    filePath = "唐诗三百首.json"
    print(filePath)
    list = check_json(filePath, "gushi/chinese-poetry/json")
    for idx in range(0, len(list)):
        print(filePath, idx)
        item = list[idx]
        print(item)
        author = item["author"]
        title = item["title"]
        paragraphs = item["paragraphs"]
        id = item["id"]
        tags = None
        if 'tags' in item:
            tags = item["tags"]

        try:
            TangShiSanBai.objects.update_or_create(author=author,
                                                   title=title,
                                                   paragraphs=paragraphs,
                                                   poet_id=id,
                                                   tags=tags)
        except ValueError:
            print(ValueError)

    end_time = time.time()
    # 关闭数据库连接
    print("耗时: {:.2f}秒".format(end_time - start_time))


def savesongci():
    start_time = time.time()
    for i in range(254, 255):
        filePath = "poet.song.{}000.json".format(i)
        print(filePath)
        list = check_json(filePath, "gushi/chinese-poetry/json")
        for idx in range(0, len(list)):
            print(filePath, idx)
            item = list[idx]
            print(item)
            author = item["author"]
            title = item["title"]
            paragraphs = item["paragraphs"]
            id = item["id"]
            try:
                SongCi.objects.update_or_create(author=author,
                                                title=title,
                                                paragraphs=paragraphs,
                                                poet_id=id)
            except ValueError:
                print(ValueError)

    end_time = time.time()
    # 关闭数据库连接
    print("耗时: {:.2f}秒".format(end_time - start_time))


def savesongciSanbai():
    start_time = time.time()
    idx = 0
    filePath = "宋词三百首.json"
    print(filePath)
    list = check_json(filePath, "gushi/chinese-poetry/ci")
    for idx in range(0, len(list)):
        print(filePath, idx)
        item = list[idx]
        print(item)
        author = item["author"]
        title = item["rhythmic"]
        paragraphs = item["paragraphs"]
        id = idx + 1
        tags = None
        if 'tags' in item:
            tags = item["tags"]
        try:
            SongCiSanBai.objects.update_or_create(author=author,
                                                  title=title,
                                                  paragraphs=paragraphs,
                                                  tags=tags,
                                                  poet_id=id)
        except ValueError:
            print(ValueError)

    end_time = time.time()
    # 关闭数据库连接
    print("耗时: {:.2f}秒".format(end_time - start_time))


def saveTangShiStrains():
    start_time = time.time()
    for i in range(0, 57):
        filePath = "poet.tang.{}000.json".format(i)
        print(filePath)
        list = check_json(filePath, "gushi/chinese-poetry/strains/json")
        for idx in range(0, len(list)):
            print(filePath, idx)
            item = list[idx]
            print(item)
            strains = item["strains"]
            id = item["id"]
            try:
                Strains.objects.update_or_create(
                    strains=strains,
                    poet_id=id,
                )
            except ValueError:
                print(ValueError)

    end_time = time.time()
    # 关闭数据库连接
    print("耗时: {:.2f}秒".format(end_time - start_time))