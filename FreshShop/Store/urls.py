from django.urls import path,re_path
from Store.views import *

from django.views.decorators.cache import cache_page

urlpatterns = [
    path('register/',register),
    path('login/',login),
    path("index/",index),
    re_path("^$",index),
    path("blank/",base),
    path("qc/",loginOut),
    path("register_store/",register_store),
    path("add_goods/",add_goods),
    re_path(r"goods_list/(?P<status>\w+)/", goods_list),
    re_path(r"^goods/(?P<goods_id>\d+)/",goods),
    re_path(r"update_goods/(?P<goods_id>\d+)/",update_goods),
    re_path(r"set_goods/(?P<status>\w+)/",set_goods),
    path("add_goods_type/",add_goods_type),
    path("delete/",delete),

    path("order_list/",cache_page(300)(order_list)),

    path(r"ajax_goods_list/",ajax_goods_list),
    path("get_add/",get_add),
    path("dingTalk/",dingTalk),

]