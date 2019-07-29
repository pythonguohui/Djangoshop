# Generated by Django 2.1.1 on 2019-07-29 03:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0002_auto_20190725_1553'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.CharField(max_length=32, verbose_name='id订单编号')),
                ('goods_count', models.IntegerField(verbose_name='商品数量')),
                ('order_price', models.FloatField(verbose_name='订单总价')),
                ('order_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.Address', verbose_name='订单地址')),
                ('order_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.Buyer', verbose_name='订单用户')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_id', models.IntegerField(verbose_name='商品id')),
                ('goods_name', models.CharField(max_length=32, verbose_name='商品名称')),
                ('goods_price', models.FloatField(verbose_name='商品价格')),
                ('goods_number', models.IntegerField(verbose_name='商品购买数量')),
                ('goods_total', models.FloatField(verbose_name='商品总价')),
                ('goods_store', models.IntegerField(verbose_name='商店id')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.Order', verbose_name='订单编号（多对一）')),
            ],
        ),
    ]
