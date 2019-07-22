import hashlib

from django.shortcuts import render
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
    return render(request,"store/index.html")

def loginOut(request):
    response=HttpResponseRedirect("/store/login/")
    response.delete_cookie("username")
    return response

def blank(request):
    return render(request,"store/blank.html")

def error404(request):
    return render(request,"store/404.html")

# Create your views here.
