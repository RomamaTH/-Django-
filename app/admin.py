from django.contrib import admin

from .models import BlogText,UserInfo,Comment
# Register your models here.



admin.site.register(BlogText)
admin.site.register(UserInfo)
admin.site.register(Comment)
