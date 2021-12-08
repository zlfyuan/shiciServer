from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, FeedBack


class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'name', 'age', 'email', 'password')}),
    )
    list_display = ('username', 'name', 'age', 'email', 'date_joined')
    search_fields = ['username', 'email']


admin.site.register(User, CustomUserAdmin)


class CustomFeedBackAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback_content', 'creat_time')


admin.site.register(FeedBack, CustomFeedBackAdmin)
