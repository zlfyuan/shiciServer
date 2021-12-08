import json
import os
import time

from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
from pypinyin import pinyin
from rest_framework import filters
from rest_framework.views import APIView
from setuptools.namespaces import flatten
from zhconv import convert_for_mw

from .models import Author, TangShi, SongCi, TangShiSanBai, Strains, SongCiSanBai, GuShiPinYins
from .serializer import TangShiSerializer, SongCiSerializer, StrainsSerializer, GuShiPinYinsSeriliazer
from utils.custom_json_response import JsonResponse
from utils.custom_pagination import LargeResultsSetPagination
from utils.custom_viewset_base import CustomViewBase


class GushiView(CustomViewBase):
    data_object = None

    def get_queryset_serializer(self, gushi_type):
        if gushi_type == "tangshi":
            instance = TangShi.objects.all().order_by('id')
            serializer = TangShiSerializer
            data_object = TangShi.objects
        elif gushi_type == "songci":
            instance = SongCi.objects.all().order_by('id')
            serializer = SongCiSerializer
            data_object = SongCi.objects
        elif gushi_type == "tangshisanbai":
            instance = TangShiSanBai.objects.all().order_by('id')
            serializer = TangShiSerializer
            data_object = TangShiSanBai.objects
        elif gushi_type == "songcisanbai":
            instance = SongCiSanBai.objects.all().order_by('id')
            serializer = SongCiSerializer
            data_object = SongCiSanBai.objects
        elif gushi_type == "pinyin":
            instance = GuShiPinYins.objects.all().order_by('id')
            serializer = GuShiPinYinsSeriliazer
            data_object = GuShiPinYins.objects
        elif gushi_type == "strains":
            instance = Strains.objects.all().order_by('id')
            serializer = StrainsSerializer
            data_object = Strains.objects
        else:
            return JsonResponse(msg="fail", code=233)
        return instance, serializer, data_object

    def list(self, request, *args, **kwargs):
        gushi_type = kwargs.pop('type', '')

        self.queryset, self.serializer_class, self.data_object = self.get_queryset_serializer(gushi_type)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        queryset = self.filter_queryset(self.get_queryset().all()[0:20])
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data, code=200, msg="success")

    def retrieve(self, request, *args, **kwargs):
        gushi_type = kwargs.pop('type', '')

        self.queryset, self.serializer_class, self.data_object = self.get_queryset_serializer(gushi_type)

        instance = self.get_object()
        # 繁体转换简体
        zh_cn_title = zh_ft_convert_zh_cn(instance.title)
        zh_cn_author = zh_ft_convert_zh_cn(instance.author)
        zh_cn_paragraphs = zh_ft_convert_zh_cn(instance.paragraphs)
        zh_cn_paragraphs = zh_cn_paragraphs.replace("\'", "\"")
        _t = self.data_object.get(poet_id=instance.poet_id)
        _t.author = zh_cn_author
        _t.title = zh_cn_title
        _t.paragraphs = zh_cn_paragraphs
        # 添加拼音
        if _t.pinyin is None:
            _list = json.loads(zh_cn_paragraphs)
            pinyi_paragraphs = []
            for i in _list:
                _pinyi_paragraphs = pinyin_convert(i)
                pinyi_paragraphs += _pinyi_paragraphs
            pinyi_instance = GuShiPinYins.objects.update_or_create(author_pinyin=pinyin_convert(zh_cn_author),
                                                                   title_pinyin=pinyin_convert(zh_cn_title),
                                                                   paragraphs_pinyin=pinyi_paragraphs)
            _t.pinyin = pinyi_instance[0]

        try:
            # 关联节奏
            if _t.strains is None and instance.poet_id is not None:
                strains = Strains.objects.get(poet_id=instance.poet_id)
                if strains is not None:
                    _t.strains = strains

            # 关联作者表
            if _t.author_id is None and instance.poet_id is not None:
                author_instance = Author.objects.get(name=instance.author)
                if author_instance is not None:
                    _t.author_id = author_instance
        except ObjectDoesNotExist as error:
            print(error, "error")
        finally:
            _t.save()
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return JsonResponse(data=serializer.data, code=200, msg="success")


    def update(self, request, *args, **kwargs):

        pk = kwargs.pop('pk', -1)
        gushi_type = kwargs.pop('type', '')
        self.queryset, self.serializer_class, self.data_object = self.get_queryset_serializer(gushi_type)
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return JsonResponse(data=serializer.data, msg="success", code=200)


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

class Search(filters.SearchFilter):
    search_param = "keyword"


class SearchView(APIView):

    def get(self, request):
        search_type = request.GET.get('type')
        source = request.GET.get('source')
        pagination_class = LargeResultsSetPagination()
        search_class = Search()

        self.search_fields = [search_type]
        print(source)
        if source == "TangShi":
            print(source, 1)
            contentlist = TangShi.objects.all().order_by('id')

            search_query = search_class.filter_queryset(request=request, queryset=contentlist, view=self)

            page_query = pagination_class.paginate_queryset(queryset=search_query, request=request, view=self)

            result_serializer = TangShiSerializer(page_query, many=True)

            page_result = pagination_class.get_paginated_response(result_serializer.data)

            return page_result
        elif source == "SongCi":
            print(source, 2)
            contentlist = SongCi.objects.all().order_by('id')

            search_query = search_class.filter_queryset(request=request, queryset=contentlist, view=self)

            page_query = pagination_class.paginate_queryset(queryset=search_query, request=request, view=self)

            result_serializer = SongCiSerializer(page_query, many=True)

            page_result = pagination_class.get_paginated_response(result_serializer.data)

            return page_result
        elif source == "TangshiSanBai":
            print(source, 3)
            contentlist = TangShiSanBai.objects.all().order_by('id')

            search_query = search_class.filter_queryset(request=request, queryset=contentlist, view=self)

            page_query = pagination_class.paginate_queryset(queryset=search_query, request=request, view=self)

            result_serializer = TangShiSerializer(page_query, many=True)

            page_result = pagination_class.get_paginated_response(result_serializer.data)

            return page_result
        elif source == "SongCiSanBai":
            print(source, 4)
            contentlist = SongCi.objects.all().order_by('id')

            search_query = search_class.filter_queryset(request=request, queryset=contentlist, view=self)

            page_query = pagination_class.paginate_queryset(queryset=search_query, request=request, view=self)

            result_serializer = SongCiSerializer(page_query, many=True)

            page_result = pagination_class.get_paginated_response(result_serializer.data)

            return page_result
        else:
            return pagination_class.get_none_page_response()

# class GushiView(APIView):
#     # queryset = TangShi.objects.all().order_by("id")
#     # serializer_class = TangShiSerializer
#     # saveAuthor()
#     def get(self, request):
#         # saveAuthor()
#         # save()
#         # saveTangShisanbai()
#         # saveTangShiStrains()
#         # savesongci()
#         # savesongciSanbai()
#         saveSongCiStrains()
#         return JsonResponse(code=233, msg="success")


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


def saveSongCiStrains():
    start_time = time.time()
    for i in range(254, 255):
        filePath = "poet.song.{}000.json".format(i)
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
