from django.urls import path,re_path
from Store.views import *
urlpatterns = [
    path('register/',register),
    path('login/',login),
    path("index/",index),
    re_path("^$",index),
    path("blank/",base),
    path("404/",error404),
    path("qc/",loginOut),
    path("register_store/",register_store),
    path("add_goods/",add_goods),
    path("goods_list/", goods_list)
]