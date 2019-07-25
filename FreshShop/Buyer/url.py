from django.urls import path,re_path
from Buyer.views import *

urlpatterns = [
    path("login/",login),
    path("index/", index),
    path("loginOut/",loginOut),
    path("register/", register),
]


urlpatterns += [
    path("base/", base),
    re_path("^$",index)
]