from django.contrib import admin

# Register your models here.
from gushi.models import TangShi, SongCi


class TangShiAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'paragraphs', 'tags')


admin.site.register(TangShi, TangShiAdmin)


class SongciAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'paragraphs', 'tags')


admin.site.register(SongCi, SongciAdmin)
