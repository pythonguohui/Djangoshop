from __future__ import absolute_import
from FreshShop.celery import app

@app.task
def taskExample():
    print('send Email ok!')

@app.task
def add(x=1,y=2):
    return x+y