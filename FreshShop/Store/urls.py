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
    path("goods_list/", goods_list),
    re_path(r"^goods/(?P<goods_id>\d+)",goods),
    re_path(r"update_goods/(?P<goods_id>\d+)",update_goods),
    re_path(r"sc/(?P<goods_id>\d+)",delete_goods),
    path("upder/",upder_goods)
]