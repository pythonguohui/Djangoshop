import time
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.db.models import Sum

from Buyer.models import *
from Store.models import *
from Store.views import set_password

from alipay import AliPay

def login(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("pwd")
        if username:
            user=Buyer.objects.filter(username=username).first()
            if user:
                web_password=set_password(password)
                if user.password == web_password:
                    response= HttpResponseRedirect("/Buyer/index/")
                    response.set_cookie("username",user.username)
                    request.session["username"]=user.username
                    response.set_cookie("user_id",user.id)
                    return response

    return render(request,"login.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        email = request.POST.get("email")

        buyer =Buyer()
        buyer.username=username
        buyer.password=set_password(password)
        buyer.email=email
        buyer.save()
        return HttpResponseRedirect("/Buyer/login")
    return render(request,"register.html")


def loginVaild(fun):
    def inner(request,*args,**kwargs):
        c_user = request.COOKIES.get("username")
        s_user = request.session.get("username")
        if c_user and s_user and c_user==s_user:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/Buyer/login")
    return inner

@loginVaild
def index(request):
    result=[]
    goods_type_list=GoodsType.objects.all()
    for goods_type in goods_type_list:
        goods_list=goods_type.goods_set.values()[:4]
        if goods_list:
            goodsType={
                "id":goods_type.id,
                "goods_name":goods_type.goods_name,
                "goods_description":goods_type.goods_description,
                "goods_image":goods_type.goods_image,
                "goods_list":goods_list
            }
            result.append(goodsType)
    return render(request,"index.html",locals())

def loginOut(request):
    response=HttpResponseRedirect("/Buyer/login")
    for key in response.cookies:
        response.delete_cookie(key)
    del request.session["username"]
    return response

def goods_list(request):
    goods_list=[]
    type_id=request.GET.get("type_id")
    goods_type=GoodsType.objects.filter(id=type_id).first()
    if goods_type:
        goodsList=goods_type.goods_set.filter(goods_upder=1)
    return  render(request,"list.html",locals())

def base(request):
    return render(request,"base.html")

def pay_result(request):
    """
    charset=utf-8
    out_trade_no=1000001
    timestamp=2019-07-27+13%3A56%3A35
    total_amount=12.00
    """
    return render(request,"pay_order.html",locals())

def pay_order(request):
    money=request.GET.get("money")
    order_id=request.GET.get("order_id")

    alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvu8nR/GDlBxY2/J4nwHxsKabC+WeCf1N0xzOXMwFfo7Fj6zsNnGSASWnMIMzF9/jqy6ypsbX/xP+b9534fHlftja3CaJ+uCHqF4g1fdH0S46tWy9yIZHaq5d7EqMIVHLaYHR/TSFPSgqpmTtk83oiUGShqtE2tDl68/mOIjqN91jCAPcTF8XXK1Tqw2+SZn4zWVTZotoIG11F3x+TWpR+yPpswXfOhZ6JMWZP7uu0wIPDL1l4sSZovYjI1v38VxUPNEn/XbfBXe7KtUd1DXfBTbbmTrtFy7hJlSAw+xD50TqujCPU1xpN/D/EWJF7GCAMAxHyKUwjWQigzSPMLX/PQIDAQAB
    -----END PUBLIC KEY-----"""

    app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
    MIIEpAIBAAKCAQEAvu8nR/GDlBxY2/J4nwHxsKabC+WeCf1N0xzOXMwFfo7Fj6zsNnGSASWnMIMzF9/jqy6ypsbX/xP+b9534fHlftja3CaJ+uCHqF4g1fdH0S46tWy9yIZHaq5d7EqMIVHLaYHR/TSFPSgqpmTtk83oiUGShqtE2tDl68/mOIjqN91jCAPcTF8XXK1Tqw2+SZn4zWVTZotoIG11F3x+TWpR+yPpswXfOhZ6JMWZP7uu0wIPDL1l4sSZovYjI1v38VxUPNEn/XbfBXe7KtUd1DXfBTbbmTrtFy7hJlSAw+xD50TqujCPU1xpN/D/EWJF7GCAMAxHyKUwjWQigzSPMLX/PQIDAQABAoIBAQC559vkZdjKposypTUjBV6RtLa0b79gVJ2pF5wqqJAU+OiNiz53iD80FLhkOOrPrTRc4dwbHPMErzAHNqKdgc0FpBn9Txz8BBCyM+xeySXJG+0X5ygmjfANhHd48eDdNGoNcdTHaJLuyCQ23YChcFShCBKmQy6Iq+uinku38j+zYZAjNbUP1QtHZkIrR36bLUfHJPfz403SV8Jz9VQ9jx6iq0KTPoEeDDm28+6Vdzqssp0zOUdUUtQJnHtmBNFvhwasJiX+rzAM62zc0cD+QCCaEuwO0y6EQapowri4RxA4MKcZn9fb6iAZ7E6YAsLMfccrcEwu7NcEeR3/xppNhoD1AoGBAPSpVIRX+pQNvzYwL0zHyfvoP24SDsetN63+6UDHFOHGreOJu4AqCsHbobBBYajtNxr8WOZh0fu4bwDx9tbL0Lja+BptEGNnccUTnynf1dxlYZMO5goDTrRaraVuPwoXFnsWP8HKvut5QvhgnE3Tv1bJOMWSRqeLDA0QAV9q+S8jAoGBAMfIZtkwraDerjVJwdn1+t7llhpQqJLeCgqXqtdbABXhB/Q7/UpOoyLOvHhznVyAbaRo0d3oeANrCYvxeCnzhxzmZmflPwPwfjBwIHpwkb7nT2Q1ArslXdn5JUa0KRoGvTBBj/V9FdCARA4cdTkzD7CB/hiOM1gIARbISOkTOy4fAoGBAKjoYjX/+znNh83kVDNg1vx3qZrXEqcd2gvgqa4UA0GgBZrKEs13uPd/JtBlQwP5yQpzXvimXe63tMLlSXGfQljsq06rLx5BY1UYp9Cj/KRsxYFeTsho4iQ3WhyU0SapK9cMVDX5P/eXPvn00NQWNMm4n94ej3LJ1ycJfrkeRCwbAoGAPsEaXVrHD2MjQaXbeIWlueJQFhAEA64vZUhi56a0DitTfkphs7ej0skxtnxKj8XfqucqFRRyrlAu/YBqCHNwm4lb3YLLGoeue7Sc3xkBDwBFlep44yRHqLJ0HRN2XbCEOOY/PBOAiK/hsLULtV3urbkHgdsZEavh+7AKBvx9eG0CgYBc4HqfA7+Lcg6FhW6corRXXlV3JfandQ7VcPKpQbHRJprjZjxKrZ/2heCTuaveM9XmBvp7xHljMN4PWqCkOia2rAl7QvOMhCNznfYck/OyeFB+ODz+7/SGQGhhiYjZybmxe5Oglm+zrl65aQiqQIM857AcwQM7SIbme7dnmJU/IQ==
    -----END RSA PRIVATE KEY-----"""

    alipay = AliPay(
        appid="2016101000652528",
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2"
    )
    # 发起支付请求
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,  # 订单号
        total_amount=str(money),  # 支付金额
        subject="生鲜交易",  # 交易主题
        return_url="http://127.0.0.1:8000/Buyer/pay_result/",
        notify_url="http://127.0.0.1:8000/Buyer/pay_result/"
    )
    order= Order.objects.get(order_id=order_id)
    order.order_status = 2
    order.save()
    return  HttpResponseRedirect ("https://openapi.alipaydev.com/gateway.do?" + order_string)

def detail(request):
    goods_id=request.GET.get("id")
    if goods_id:
        goods=Goods.objects.filter(id=goods_id).first()
        if goods:
            return render(request,"detail.html",locals())
    return HttpResponseRedirect("没有该商品")


def setOrderId(user_id,goods_id,store_id):
    result=time.strftime("%Y%m%d%H%M%S",time.localtime())
    return result+str(user_id)+str(goods_id)+str(store_id)

def place_order(request):
    if request.method == "POST":
        count= int(request.POST.get("count"))
        goods_id=request.POST.get("goods_id")
        user_id=request.COOKIES.get("user_id")

        goods=Goods.objects.get(id=goods_id)
        store_id=goods.store_id.id
        price=goods.goods_price

        order =Order()
        order.order_id=setOrderId(str(user_id),str(goods_id),str(store_id))
        order.goods_count=count
        order.order_user=Buyer.objects.get(id=user_id)
        order.order_price=count * price
        order.order_status=1
        order.save()

        order_detail=OrderDetail()
        order_detail.order_id=order
        order_detail.goods_id=goods_id
        order_detail.goods_name=goods.goods_name
        order_detail.goods_price=goods.goods_price
        order_detail.goods_number=count
        order_detail.goods_total=count*goods.goods_price
        order_detail.goods_store=store_id
        order_detail.goods_images=goods.goods_image
        order_detail.save()

        detail=[order_detail]
        return render(request,"place_order.html",locals())
    else:
        order_id=request.GET.get("order_id")
        if order_id:
            order=Order.objects.get(id=order_id)
            detail=order.orderdetail_set.all()
            return render(request,"place_order.html",locals())
        else:
            return HttpResponse("非法请求")

def querenfahuo(request):
    order_id=request.GET.get("order")
    order = Order.objects.get(order=order_id)
    order.order_status = 2

def add_cart(request):
    result={"state":"error","data":""}
    if request.method=="POST":
        count=int(request.POST.get("count"))
        goods_id=request.POST.get("goods_id")
        goods=Goods.objects.get(id=int(goods_id))

        user_id=request.COOKIES.get("user_id")

        cart=Cart()
        cart.goods_name=goods.goods_name
        cart.goods_price=goods.goods_price
        cart.goods_total=goods.goods_price*count
        cart.goods_number=count
        cart.goods_picture=goods.goods_image
        cart.goods_id=goods_id
        cart.goods_store=goods.store_id.id
        cart.user_id=user_id
        cart.save()
        result["state"]="success"
        result["data"]="商品添加成功"
    else:
        result["data"]="请求错误"
    return JsonResponse(result)

def cart(request):
    user_id=request.COOKIES.get("user_id")
    goods_list=Cart.objects.filter(user_id=user_id)
    if request.method == "POST":
        post_data = request.POST
        cart_data = []
        for k,v in post_data.items():
            if k .startswith("goods_"):
                cart_data.append(Cart.objects.get(id=int(v)))
        goods_count=len(cart_data)
        goods_total=sum([int(i.goods_total) for i in  cart_data])

        # cart_data =[]
        # for k,v in post_data.items():
        #     if k.startswith("goods_"):
        #         cart_data.append(int(v))
        # cart_goods=Cart.objects.filter(id__in=cart_data).aggregate(Sum("goods_total"))
        # print(cart_goods)

        order =Order()
        order.order_id=setOrderId(user_id,goods_count,"2")
        order.goods_count=goods_count
        order.order_user=Buyer.objects.get(id=user_id)
        order.order_status=1
        order.order_price=goods_total
        order.save()

        for detail in cart_data:
            order_detail=OrderDetail()
            order_detail.order_id=order
            order_detail.goods_id=detail.goods_id
            order_detail.goods_name=detail.goods_name
            order_detail.goods_price=detail.goods_price
            order_detail.goods_number=detail.goods_number
            order_detail.goods_total=detail.goods_total
            order_detail.goods_store=detail.goods_store
            order_detail.goods_images=detail.goods_picture
            order_detail.save()

            url="/Buyer/place_order/?order_id=%s"%order.id
            return HttpResponseRedirect(url)

    return render(request,"cart.html",locals())

# Create your views here.
