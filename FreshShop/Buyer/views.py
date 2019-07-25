from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect

from Buyer.models import *
from Store.models import *
from Store.views import set_password


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
    goods=GoodsType.objects.all()
    return render(request,"index.html",locals())

def loginOut(request):
    response=HttpResponseRedirect("/Buyer/login")
    for key in response.cookies:
        response.delete_cookie(key)
    del request.session["username"]
    return response





def base(request):
    return render(request,"base.html")

# Create your views here.
