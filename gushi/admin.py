from django.contrib import admin

# Register your models here.
from gushi.models import TangShi, SongCi, Strains


class StrainsAdmin(admin.ModelAdmin):
    list_display = ('strains', 'last_change_date')


admin.site.register(Strains, StrainsAdmin)


class TangShiAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'paragraphs', 'tags', 'last_change_date')


admin.site.register(TangShi, TangShiAdmin)


class SongciAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'paragraphs', 'tags', 'last_change_date')


admin.site.register(SongCi, SongciAdmin)
