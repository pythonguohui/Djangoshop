import hashlib

from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect

from Store.models import *

def set_password(password):
    md5=hashlib.md5()
    md5.update(password.encode())
    result=md5.hexdigest()
    return  result

def register(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        if username and password:
            seller=Seller()
            seller.username=username
            seller.password=set_password(password)
            seller.save()
            return HttpResponseRedirect("/store/login/")
    return render(request,"store/register.html")

def login(request):
    response=render(request,"store/login.html")
    response.set_cookie("login_form","login_page")
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user=Seller.objects.filter(username=username).first()
            if user:
                web_password=set_password(password)
                cookies=request.COOKIES.get("login_form")
                if user.password==web_password and cookies=="login_page":
                    result=HttpResponseRedirect("/store/index/")
                    result.set_cookie("username",username)
                    result.set_cookie("user_id",user.id)
                    request.session["username"]=username
                    return result
    return response

def loginValid(fun):
    def inner(request,*args,**kwargs):
        c_user=request.COOKIES.get("username")
        s_user=request.session.get("username")
        if c_user and s_user:
            user=Seller.objects.filter(username=c_user).first()
            if user and c_user==s_user:
                return fun(request,*args,**kwargs)
        return HttpResponseRedirect("/store/login/")
    return inner

@loginValid
def index(request):
    user_id=request.COOKIES.get("user_id")
    if user_id:
        user_id=int(user_id)
    else:
        user_id=0
    store=Store.objects.filter(user_id=user_id).first()
    if store:
        is_store = 1
    else:
        is_store = 0
    return render(request,"store/index.html",{"is_store":is_store})

def loginOut(request):
    response=HttpResponseRedirect("/store/login/")
    response.delete_cookie("username")
    return response

def base(request):
    return render(request, "store/base.html")

def error404(request):
    return render(request,"store/404.html")


def register_store(request):
    type_list=StoreType.objects.all()
    if request.method=="POST":
        post_data=request.POST
        store_name = post_data.get("store_name")
        store_address = post_data.get("store_address")
        store_description = post_data.get("store_description")
        store_phone = post_data.get("store_phone")
        store_money = post_data.get("store_money")

        user_id=int(request.COOKIES.get("user_id"))
        type_lists=post_data.getlist("type")

        store_logo = request.FILES.get("store_logo")

        store=Store()
        store.store_name=store_name
        store.store_address=store_address
        store.store_description=store_description
        store.store_phone=store_phone
        store.store_money=store_money
        store.user_id=user_id
        store.store_logo=store_logo
        store.save()

        for i in type_lists:
            store_type=StoreType.objects.get(id=i)
            store.type.add(store_type)
        store.save()
    return render(request,"store/register_store.html",locals())

def add_goods(request):
    if request.method == "POST":
        goods_name= request.POST.get("goods_name")
        goods_price= request.POST.get("goods_price")
        goods_number = request.POST.get("goods_number")
        goods_description = request.POST.get("goods_description")
        goods_date = request.POST.get("goods_date")
        goods_safeDate = request.POST.get("goods_safeDate")
        goods_store = request.POST.get("goods_store")
        goods_image = request.FILES.get("goods_image")

        goods=Goods()
        goods.goods_name=goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        goods.goods_image=goods_image
        goods.save()
        goods.store_id.add(
            Store.objects.get(id=int(goods_store))
        )
        goods.save()
    return render(request,"store/add_goods.html")


def goods_list(request):
    keywords=request.GET.get("keywords","")
    page_num=request.GET.get("page_num",1)
    if keywords:
        goods_list=Goods.objects.filter(goods_name__contains=keywords)
    else:
        goods_list=Goods.objects.all()
    paginator=Paginator(goods_list,3)
    page=paginator.page(int(page_num))
    page_range=paginator.page_range

    count_goods=Goods.objects.all().count()

    count=goods_list.count()
    page_end=count//3 if count//3==0 else count//3+1

    page_num=int(page_num)
    if page_num ==page_end:
        next_num=page_num
    else:
        next_num=page_num+1

    if page_num == 1:
        before_num=page_num
    else:
        before_num=page_num-1
    return render(request,"store/goods_list.html",{"page":page,"page_range":page_range,"keywords":keywords,
                                                   "page_num":page_num,"page_end":page_end,"count_goods":count_goods,
                                                   "next_num":next_num,"before_num":before_num})




# Create your views here.
