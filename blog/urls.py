"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 用户的界面
    path('homepage/', views.home_page),
    path('reading/<int:nid>/', views.reading),

    # 登录和注册
    path("login/", views.login),
    path("register/", views.register),
    path("logout/", views.logout),

    # 用户的喜欢和收藏列表
    path("favourite/", views.favourite),
    path("collect/", views.collect),
    path("delete/collect/", views.delete_collect),
    path("delete/favourite/", views.delete_favourite),
    path("my/Favourite/", views.my_favourite),
    path("my/Collect/", views.my_collect),

    # 评论管理
    path("add/comment/", views.add_comment),
    path("delete/comment/", views.delete_comment),

    #     分类
    path("type/<int:nid>/", views.type_choice),

]
