from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.


class BlogText(models.Model):
    title = models.CharField(verbose_name="标题", max_length=100)
    body = models.TextField(verbose_name="内容")
    total_views = models.PositiveIntegerField(default=0,verbose_name="浏览次数")
    create_time = models.DateTimeField(default=timezone.now,verbose_name="创建时间")
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    type_choices = (
        (1, "python"),
        (2, "java"),
        (3, "其他"),
    )
    page_type = models.SmallIntegerField(verbose_name="类型",choices=type_choices,default=3)

    def __str__(self):
        return self.title

class UserInfo(models.Model):
    user_name = models.CharField(verbose_name="用户名",max_length=100)
    user_password = models.CharField(verbose_name="密码",max_length=100)

    def __str__(self):
        return self.user_name

class Comment(models.Model):
    user = models.CharField(max_length=100)
    context = models.TextField()
    page_id = models.ForeignKey(to="BlogText", to_field="id",on_delete=models.CASCADE)
    create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")

    def __str__(self):
        return self.context

class UserFavourite(models.Model):
    page_id = models.ForeignKey(to="BlogText", to_field="id", on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    like = models.BooleanField(default=True)

class UserCollect(models.Model):
    page_id = models.ForeignKey(to="BlogText", to_field="id", on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    collect = models.BooleanField(default=True)

