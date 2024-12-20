from django.db import models


class Author(models.Model):
    DYNASTY_TYPE_CHOICE = (
        (0, "未知"),
        (1, "唐"),
        (2, "宋"),
        (3, "元"),
        (4, "明"),
        (5, "清"),
    )

    name = models.CharField(max_length=100, verbose_name="作者")
    author_id = models.CharField(max_length=100, verbose_name="原始_ id")
    desc = models.TextField(max_length=2048 * 2, null=True, default="", verbose_name="作者描述")
    dynasty = models.IntegerField(choices=DYNASTY_TYPE_CHOICE, verbose_name="作者所处年代")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "古诗作者"
        ordering = ['id', '-create_time']


class Strains(models.Model):
    strains = models.TextField(max_length=5000, verbose_name="宋词内容")
    poet_id = models.CharField(max_length=100, verbose_name="宋词原始_ id")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_change_date = models.DateTimeField(auto_now=True, verbose_name="最后修改日期")

    class Meta:
        verbose_name = "节奏，押韵"
        ordering = ['id']


class GuShiPinYins(models.Model):
    author_pinyin = models.CharField(max_length=300, null=True, verbose_name="作者_pinyin")
    title_pinyin = models.CharField(max_length=300, null=True, verbose_name="标题_pinyin")
    paragraphs_pinyin = models.TextField(max_length=5000, null=True, verbose_name="内容_pinyin")
    # poet_id = models.CharField(max_length=100, null=True, verbose_name="宋词原始_ id")

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_change_date = models.DateTimeField(auto_now=True, verbose_name="最后修改日期")

    class Meta:
        verbose_name = "拼音 表"
        ordering = ['id']


class TangShi(models.Model):
    author = models.CharField(max_length=300, verbose_name="古诗作者")
    title = models.CharField(max_length=300, verbose_name="古诗标题")
    paragraphs = models.TextField(max_length=5000, verbose_name="古诗内容")
    poet_id = models.CharField(max_length=100, verbose_name="古诗原始_ id")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_change_date = models.DateTimeField(auto_now=True, verbose_name="最后修改日期")
    tags = models.CharField(max_length=300, null=True, verbose_name="古诗tag")
    pinyin = models.OneToOneField(to=GuShiPinYins, null=True, on_delete=models.CASCADE, verbose_name="拼音")
    strains = models.OneToOneField(to=Strains, null=True, on_delete=models.CASCADE, verbose_name="节奏")
    author_id = models.OneToOneField(to=Author, null=True, on_delete=models.CASCADE, verbose_name="作者")

    class Meta:
        verbose_name = "唐诗"
        ordering = ['id']


class TangShiSanBai(TangShi):
    class Meta:
        verbose_name = "唐诗三百首"
        ordering = ['id']


class SongCi(models.Model):
    author = models.CharField(max_length=300, verbose_name="宋词作者")
    title = models.CharField(max_length=300, verbose_name="宋词标题")
    paragraphs = models.TextField(max_length=5000, verbose_name="宋词内容")
    poet_id = models.CharField(max_length=100, verbose_name="宋词原始_ id")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_change_date = models.DateTimeField(auto_now=True, verbose_name="最后修改日期")
    tags = models.CharField(max_length=300, null=True, verbose_name="宋词tag")
    pinyin = models.OneToOneField(to=GuShiPinYins, null=True, on_delete=models.CASCADE, verbose_name="拼音")
    strains = models.OneToOneField(to=Strains, null=True, on_delete=models.CASCADE, verbose_name="节奏")
    author_id = models.OneToOneField(to=Author, null=True, on_delete=models.CASCADE, verbose_name="作者")

    class Meta:
        verbose_name = "宋词"
        ordering = ['id']


class SongCiSanBai(SongCi):
    class Meta:
        verbose_name = "宋词三百首"
        ordering = ['id']




class YuanQu(models.Model):
    author = models.CharField(max_length=300, verbose_name="元曲作者")
    title = models.CharField(max_length=300, verbose_name="元曲标题")
    poet_id = models.CharField(max_length=100, null=True, verbose_name="元曲原始_ id")
    paragraphs = models.TextField(max_length=5000, verbose_name="元曲内容")
    dynasty = models.CharField(max_length=100, verbose_name="元曲")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_change_date = models.DateTimeField(auto_now=True, verbose_name="最后修改日期")
    tags = models.CharField(max_length=300, null=True, verbose_name="元曲tag")
    pinyin = models.OneToOneField(to=GuShiPinYins, null=True, on_delete=models.CASCADE, verbose_name="拼音")
    strains = models.OneToOneField(to=Strains, null=True, on_delete=models.CASCADE, verbose_name="节奏")
    author_id = models.OneToOneField(to=Author, null=True, on_delete=models.CASCADE, verbose_name="作者")

    class Meta:
        verbose_name = "元曲"
        ordering = ['id']

class ShiJing(models.Model):
    author = models.CharField(max_length=300, verbose_name="诗经作者")
    title = models.CharField(max_length=300, verbose_name="诗经标题")
    poet_id = models.CharField(max_length=100, null=True, verbose_name="诗经原始_ id")
    paragraphs = models.TextField(max_length=5000, verbose_name="诗经内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_change_date = models.DateTimeField(auto_now=True, verbose_name="最后修改日期")
    tags = models.CharField(max_length=300, null=True, verbose_name="诗经tag")
    pinyin = models.OneToOneField(to=GuShiPinYins, null=True, on_delete=models.CASCADE, verbose_name="拼音")
    strains = models.OneToOneField(to=Strains, null=True, on_delete=models.CASCADE, verbose_name="节奏")
    author_id = models.OneToOneField(to=Author, null=True, on_delete=models.CASCADE, verbose_name="作者")

class Meta:
        verbose_name = "诗经"
        ordering = ['id']

class LunYu(models.Model):
    author = models.CharField(max_length=300, verbose_name="论语作者")
    title = models.CharField(max_length=300, verbose_name="论语标题")
    poet_id = models.CharField(max_length=100, null=True, verbose_name="论语原始_ id")
    paragraphs = models.TextField(max_length=5000, verbose_name="论语内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_change_date = models.DateTimeField(auto_now=True, verbose_name="最后修改日期")
    tags = models.CharField(max_length=300, null=True, verbose_name="论语tag")
    pinyin = models.OneToOneField(to=GuShiPinYins, null=True, on_delete=models.CASCADE, verbose_name="拼音")
    strains = models.OneToOneField(to=Strains, null=True, on_delete=models.CASCADE, verbose_name="节奏")
    author_id = models.OneToOneField(to=Author, null=True, on_delete=models.CASCADE, verbose_name="作者")


class Meta:
        verbose_name = "论语"
        ordering = ['id']