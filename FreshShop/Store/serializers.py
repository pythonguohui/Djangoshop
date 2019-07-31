from rest_framework import serializers
from Store.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Goods
        fields=['goods_name','goods_price','goods_number','goods_description','goods_safeDate','goods_date','id']

class GoodsTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= GoodsType
        fields=['goods_name','goods_description']