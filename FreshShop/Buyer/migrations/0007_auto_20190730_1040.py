# Generated by Django 2.1.1 on 2019-07-30 02:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0006_auto_20190730_0958'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='User_id',
            new_name='user_id',
        ),
    ]
