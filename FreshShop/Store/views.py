import hashlib


from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect

from Buyer.models import OrderDetail

def set_password(password):  #设置密码加密
    md5=hashlib.md5()
    md5.update(password.encode())
    result=md5.hexdigest()
    return  result

def register(request):   #注册函数
    if request.method=="POST":    #如果数据是POST类型则执行下一步
        username=request.POST.get("username")   #获取用户名
        password=request.POST.get("password")   #获取密码
        if username and password:               #如果用户名和密码存在
            seller=Seller()                     #实例化数据库
            seller.username=username            #把用户名存储进库中
            seller.password=set_password(password)          #把密码存储进库中
            seller.save()                       #保存
            return HttpResponseRedirect("/store/login/")        #重定向地址
    return render(request,"store/register.html")

def login(request):             #登录函数
    response=render(request,"store/login.html")                     #登录页面
    response.set_cookie("login_form","login_page")                  #给登录页面设置COOKIE
    if request.method=="POST":                                      #如果数据是POST类型
        username = request.POST.get("username")                     #获取用户名
        password = request.POST.get("password")                     #获取密码
        if username and password:                                   #如果用户名和密码存在
            user=Seller.objects.filter(username=username).first()           #通过用户名库来搜索是否存在此用户
            if user:                                                        #如果存在此用户
                web_password=set_password(password)                         #密码为输入后的加密密码
                cookies=request.COOKIES.get("login_form")                   #通过页面获得COOKIE
                if user.password==web_password and cookies=="login_page":   #如果密码正确，COOKIE正确执行下一步
                    result=HttpResponseRedirect("/store/index/")            #重定向页面到首页
                    result.set_cookie("username",username)                  #设置COOKIE 值为用户名
                    result.set_cookie("user_id",user.id)                    #设置COOKIE 值为id
                    request.session["username"]=username                    #设置session
                    store=Store.objects.filter(user_id=user.id).first()     #通过ID查询到商铺是否有该用户
                    if store:                                               #如果有该用户
                        result.set_cookie("has_store",store.id)             #设置一个COOKIE校验，值为商铺id
                    else:                                                   #如果没有该用户
                        result.set_cookie("has_store","")                   #设置一个COOKIE校验，值为空
                    return result
    return response

def loginValid(fun):                                            #登录校验装饰器
    def inner(request,*args,**kwargs):                          #内函数
        c_user=request.COOKIES.get("username")                  #获取COOKIE
        s_user=request.session.get("username")                  #获取session
        if c_user and s_user:                                   #如果cookie和session存在
            user=Seller.objects.filter(username=c_user).first()     #查询用户名库是否有这个COOKIE
            if user and c_user==s_user:                            #如果有这个用户
                return fun(request,*args,**kwargs)                  #返回这个调用函数
        return HttpResponseRedirect("/store/login/")           #如果不存在，重定向页面到登录页面
    return inner

@loginValid
def index(request):
    return render(request,"store/index.html")

def loginOut(request):                                                  #退出函数
    response=HttpResponseRedirect("/store/login/")
    for key in request.COOKIES:
        response.delete_cookie(key)                                  #删除COOKIE
    return response

def base(request):                                              #继承页函数
    return render(request, "store/base.html")

def register_store(request):                                   #注册商铺
    type_list=StoreType.objects.all()                          #查询商铺类型库里所有信息
    if request.method=="POST":                                 #如果请求类型为POST
        post_data=request.POST
        store_name = post_data.get("store_name")                #获取商铺名称
        store_address = post_data.get("store_address")          #获取商铺地址
        store_description = post_data.get("store_description")  #获取商铺描述
        store_phone = post_data.get("store_phone")              #获取商铺电话
        store_money = post_data.get("store_money")              #获取商铺注册资金

        user_id=int(request.COOKIES.get("user_id"))             #通过COOKIE获取id
        type_lists=post_data.getlist("type")                    #获取商铺类型    getlist得到的将变列表

        store_logo = request.FILES.get("store_logo")            #获取图片

        store=Store()                                           #实例化商铺库
        store.store_name=store_name                             #传入商铺名称
        store.store_address=store_address                       #传入商铺地址
        store.store_description=store_description               #传入商铺描述
        store.store_phone=store_phone                           #传入商铺电话
        store.store_money=store_money                           #传入商铺注册资金
        store.user_id=user_id                                   #传入商铺ID
        store.store_logo=store_logo                             #传入商铺图片
        store.save()                                            #商铺库存储

        for i in type_lists:                                    #遍历注册请求时传入过来的商铺类型
            store_type=StoreType.objects.get(id=i)             #商铺类型库与其商铺类型ID对应
            store.type.add(store_type)                          #把商铺类型挨个添加进商铺
        store.save()                                            #保存商铺
        response = HttpResponseRedirect("/store/index/")        #重定向页面到首页
        response.set_cookie("has_store",store.id)               #添加cookie 值为商铺id
        return response                                         #返回
    return render(request,"store/register_store.html",locals())

def add_goods(request):                                         #增加商品函数
    goods_type_list=GoodsType.objects.all()
    if request.method == "POST":
        goods_name= request.POST.get("goods_name")                #获取商品名称
        goods_price= request.POST.get("goods_price")
        goods_number = request.POST.get("goods_number")
        goods_description = request.POST.get("goods_description")
        goods_date = request.POST.get("goods_date")
        goods_safeDate = request.POST.get("goods_safeDate")
        goods_type=request.POST.get("goods_type")
        goods_store = request.COOKIES.get("has_store")              #通过COOKIE中商铺ID来获取商铺
        goods_image = request.FILES.get("goods_image")

        goods=Goods()                                           #实例化商品库
        goods.goods_name=goods_name                             #前端数据存入后端商品库
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        goods.goods_image=goods_image
        goods.goods_type=GoodsType.objects.get(id=int(goods_type))
        goods.store_id=Store.objects.get(id=int(goods_store))
        goods.save()
        return HttpResponseRedirect("/store/goods_list/up/")
    return render(request,"store/add_goods.html",locals())


def goods_list(request,status):                                                    #商铺列表函数
    if status == "up":
        status_num=1
    else:
        status_num=0
    keywords=request.GET.get("keywords","")                             #获取搜索内容
    page_num=request.GET.get("page_num",1)                               #获取页码，默认为第一页
    store_id =request.COOKIES.get("has_store")                          #获取商铺ID
    store =Store.objects.get(id=int(store_id))                          #获取商铺
    if keywords:
        goods_list=store.goods_set.filter(goods_name__contains=keywords,goods_upder=status_num)    #存在就查询包含该内容的内容
    else:
        goods_list=store.goods_set.filter(goods_upder=status_num)                     #不存在就查询所有
    paginator=Paginator(goods_list,3)                         #把所有信息在每页展示3条
    page=paginator.page(int(page_num))                         #显示请求页码的当页信息
    page_range=paginator.page_range                             #显示页码范围

    count_goods=len(goods_list)                     #获得信息长度

    count=goods_list.count()                        #统计信息次数
    page_end=count//3 if count//3==0 else count//3+1            #三元表达式 如果能被3整除 就显示被3整除的页数，如果不能，页数加1

    page_num=int(page_num)                          #转化页数为INT类型
    #下一页
    if page_num ==page_end:
        next_num=page_num
    else:
        next_num=page_num+1
    #上一页
    if page_num == 1:
        before_num=page_num
    else:
        before_num=page_num-1
    return render(request,"store/goods_list.html",{"page":page,"page_range":page_range,"keywords":keywords,
                                                   "page_num":page_num,"page_end":page_end,"count_goods":count_goods,
                                                   "next_num":next_num,"before_num":before_num,"status":status})


def goods(request,goods_id):                                            #商品函数
    goods_data=Goods.objects.filter(id=goods_id).first                  #通过商品库查询所有商品数据
    return render(request,"store/goods.html",locals())

def update_goods(request,goods_id):                                         #修改商品函数
    goods_data = Goods.objects.filter(id=goods_id).first                    #通过商品库查询所有商品数据
    if request.method == "POST":
        goods_name = request.POST.get("goods_name")                         #获取商品名称
        goods_price = request.POST.get("goods_price")
        goods_number = request.POST.get("goods_number")
        goods_description = request.POST.get("goods_description")
        goods_date = request.POST.get("goods_date")
        goods_safeDate = request.POST.get("goods_safeDate")
        goods_image = request.FILES.get("goods_image")

        goods = Goods.objects.get(id= int(goods_id))                     #通过传入进来的商品id找到商品库中商品所有信息
        goods.goods_name = goods_name                                       #存储到对应字段
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        if goods_image:
            goods.goods_image = goods_image
        goods.save()
        return HttpResponseRedirect("/store/goods/%s"%goods_id)
    return render(request,"store/update_goods.html",locals())



def set_goods(request,status):
    if status == "up":
        status_num=1
    else:
        status_num=0
    id=request.GET.get("id")
    referer=request.META.get("HTTP_REFERER")
    if id:
        goods=Goods.objects.filter(id=id).first()
        if status =="delete":
            goods.delete()
        else:
            goods.goods_upder=status_num
            goods.save()
    return HttpResponseRedirect(referer)

def add_goods_type(request):
    goods=GoodsType.objects.all()
    if request.method=="POST":
        name=request.POST.get("name")
        description=request.POST.get("description")
        picture=request.FILES.get("picture")
        if name and description :
            types=GoodsType()
            types.goods_name=name
            types.goods_description=description
            types.goods_image=picture
            types.save()
            return HttpResponseRedirect("/store/add_goods_type/")
    return render(request,"store/add_goods_type.html",locals())

def delete(request):
    id=request.GET.get("id")
    good = GoodsType.objects.get(id=int(id))
    good.delete()
    return HttpResponseRedirect("/store/add_goods_type/")

def order_list(request):
    store_id=request.COOKIES.get("has_store")
    order_list=OrderDetail.objects.filter(order_id__order_status=2,goods_store=store_id)
    return render(request,"store/order_list.html",locals())

from rest_framework import  viewsets
from Store.serializers import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class=UserSerializer


class TypeViewSet(viewsets.ModelViewSet):
    queryset = GoodsType.objects.all()
    serializer_class=GoodsTypeSerializer

def ajax_goods_list(request):
    return render(request,"store/ajax_goods_list.html")


# Create your views here.