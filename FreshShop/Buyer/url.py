from django.urls import path,re_path
from Buyer.views import *

urlpatterns = [
    path("login/",login),
    path("index/", index),
    path("loginOut/",loginOut),
    path("register/", register),
    path("list/", goods_list),
    path("detail/",detail),
    path("place_order/",place_order),
    path("cart/",cart),
    path("add_cart/", add_cart),
]


urlpatterns += [
    path("base/", base),
    re_path("^$",index),
    path("pay_order/",pay_order),
    path("pay_result/",pay_result)
]