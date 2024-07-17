import json
from django import forms
from django.shortcuts import render, redirect
from app import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app.utils.Pagination import Pagination
from app.utils.bootstrap import BootStrapModelForm



# Create your views here.

# 首页展示
def home_page(request):
    # 最新的文章
    page = models.BlogText.objects.order_by('-id')[:5]
    # 最热的文章
    hot_page = models.BlogText.objects.order_by('-total_views')[:5]

    queryset = models.BlogText.objects.all()

    page_object = Pagination(request, queryset, page_size=5)

    context = {
        "title": "个人博客主页",
        'page': page,
        'hot': hot_page,

        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }

    return render(request, 'home_page.html', context)


# 阅读博客
def reading(request, nid):
    page = models.BlogText.objects.filter(id=nid).first()
    comment = models.Comment.objects.filter(page_id=nid).order_by("-create_time").all()
    comments_sum = models.Comment.objects.count()

    page.total_views += 1
    page.save(update_fields=['total_views'])
    yes_no = request.session.get("info")

    if yes_no is not None:
        name = request.session.get("info").get("name")
        favourite_exist = models.UserFavourite.objects.filter(page_id=nid, user=name).exists()
        collect_exist = models.UserCollect.objects.filter(page_id=nid, user=name).exists()

        context = {
            "comments_sum":comments_sum,
            "comments":comment,
            "page": page,
            "title": page.title,
            "favourite_exist": favourite_exist,
            "collect_exist": collect_exist
        }
    else:
        context = {
            "comments_sum": comments_sum,
            "comments": comment,
            "page": page,
            "title": page.title,
            "favourite_exist": False,
            "collect_exist": False
        }
    return render(request, 'reading.html', context)


# 登录
@csrf_exempt
def login(request):
    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    obj = models.UserInfo.objects.filter(user_name=user, user_password=pwd).first()
    if not obj:
        status = False
        name = " 我 的 "

    else:
        status = True
        name = user
        request.session["info"] = {
            "id": obj.id,
            "name": user,
        }

    data_dict = {
        "status": status,
        "name": name

    }

    return JsonResponse(data_dict)


# 注册功能
class FormUserInfo(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.UserInfo
        fields = "__all__"
        exclude = ["id"]
        widgets = {
            "user_password": forms.PasswordInput()
        }


def register(request):
    if request.method == "GET":
        form = FormUserInfo
        error = " "
        context = {
            "form": form,
            "error": error
        }
        return render(request, 'register.html', context)
    form = FormUserInfo(data=request.POST)
    if form.is_valid():
        pwd = form.cleaned_data.get("user_password")
        name = form.cleaned_data.get("user_name")
        exists = models.UserInfo.objects.filter(user_name=name).exists()
        if pwd != form.cleaned_data.get("confirm_password"):
            form = FormUserInfo
            error1 = " 两次密码不一致 "
            context = {
                "form": form,
                "error": error1
            }
            return render(request, 'register.html', context)
        if exists:
            form = FormUserInfo
            error2 = " 用户名已经存在 "
            context = {
                "form": form,
                "error": error2
            }
            return render(request, 'register.html', context)
        form.save()
        return redirect('/homepage/')


# 退出
def logout(request):
    request.session.clear()
    return redirect("/homepage/")


# 点赞
@csrf_exempt
def favourite(request):
    page_title = request.POST.get("page")
    user_name = request.POST.get("name")
    page_table = models.BlogText.objects.filter(title=page_title).first()
    page_id = page_table.id
    exist = models.UserFavourite.objects.filter(page_id=page_id, user=user_name).exists()

    if exist:
        context = {
            "status": False,
        }
    else:
        favourite = models.UserFavourite.objects.create(
            page_id=page_table,  # 使用BlogText实例，而不是id
            user=user_name,
            like=True
        )
        context = {
            "status": True,
        }

    return JsonResponse(context)


# 收藏
@csrf_exempt
def collect(request):
    page_title = request.POST.get("page")
    user_name = request.POST.get("name")
    page_table = models.BlogText.objects.filter(title=page_title).first()
    page_id = page_table.id
    exist = models.UserCollect.objects.filter(page_id=page_id, user=user_name).exists()

    if exist:
        context = {
            "status": False,
        }
    else:
        collect = models.UserCollect.objects.create(
            page_id=page_table,
            user=user_name,
            collect=True
        )
        context = {
            "status": True,
        }

    return JsonResponse(context)


@csrf_exempt
def delete_collect(request):
    page_title = request.POST.get("page")
    user_name = request.POST.get("name")
    page_table = models.BlogText.objects.filter(title=page_title).first()
    page_id = page_table.id

    models.UserCollect.objects.filter(page_id=page_id, user=user_name).delete()

    return JsonResponse({"status": True})


@csrf_exempt
def delete_favourite(request):
    page_title = request.POST.get("page")
    user_name = request.POST.get("name")
    page_table = models.BlogText.objects.filter(title=page_title).first()
    page_id = page_table.id

    models.UserFavourite.objects.filter(page_id=page_id, user=user_name).delete()

    return JsonResponse({"status": True})


def my_favourite(request):
    name = request.session.get("info", {}).get("name")
    form = models.UserFavourite.objects.filter(user=name).all()
    page_object = Pagination(request, form, page_size=10)
    context = {
        "title": name + "的喜欢界面",
        "table_head": name + "的喜欢列表",
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }

    return render(request, "my_favourite.html", context)


def my_collect(request):
    name = request.session.get("info", {}).get("name")
    form = models.UserCollect.objects.filter(user=name).all()
    page_object = Pagination(request, form, page_size=10)
    context = {
        "title": name + "的收藏界面",
        "table_head": name + "的收藏列表",
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }

    return render(request, "my_collect.html", context)


def type_choice(request, nid):
    form = models.BlogText.objects.filter(page_type=nid).all()
    page_object = Pagination(request, form, page_size=10)
    for choice_id, choice_label in models.BlogText.type_choices:
        if choice_id == nid:
            t =  choice_label
    context = {
        "title": "分类"+"--"+t,
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }

    return render(request, "type.html", context)

@csrf_exempt
def add_comment(request):
    page_title = request.POST.get("title")
    user_name = request.POST.get("user")
    page_table = models.BlogText.objects.filter(title=page_title).first()
    comment = request.POST.get("context")

    comment = models.Comment.objects.create(
        page_id=page_table,  # 使用BlogText实例，而不是id
        user=user_name,
        context= comment
    )

    return JsonResponse({ "status": True})
@csrf_exempt
def delete_comment(request):
    name = request.POST.get("name")
    title = request.POST.get("title")
    page = models.BlogText.objects.filter(title=title).first()
    page_id = page.id
    models.Comment.objects.filter(user=name,page_id=page_id).delete()
    return JsonResponse({"status": True})
