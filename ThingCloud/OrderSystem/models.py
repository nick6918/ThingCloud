# -*- coding: utf-8 -*-

from django.db import models
from AccountSystem.models import User
from CloudList.models import User_Address

# Create your models here.
class Order(models.Model):

    oid = models.AutoField(primary_key=True)
    addr = models.ForeignKey(User_Address)
    user = models.ForeignKey(User)
    notes = models.CharField(max_length=300)
    fee = models.FloatField()
    typeid = models.IntegerField()
    itemList = models.CharField(max_length=200)
    state = models.IntegerField()
    create_time = models.DateTimeField()
    paid_time = models.DateTimeField()
    finish_time = models.DateTimeField()
    prepayid = models.CharField(max_length=50)
    signature = models.CharField(max_length=50)
    showid = models.CharField(max_length=50)

    class Meta:

        db_table = "orders"

class Complaint(models.Model):
    cmpid = models.AutoField(primary_key=True)
    state = models.IntegerField()
    notes = models.CharField(max_length=300)
    user = models.ForeignKey(User)
    order = models.ForeignKey(Order)

    class Meta:
        db_table = "Complaints"

class VIPOrder(models.Model):
    """
        Order to buy VIP.
    """

    void = models.AutoField(primary_key=True)
    month = models.IntegerField()
    level = models.IntegerField()
    user = models.ForeignKey(User)
    prepayid = models.CharField(max_length=50)
    fee = models.CharField(max_length=50)
    #state == 0, 未支付, state = 1, 已支付， state = 2， 支付处理中
    state = models.IntegerField()

    class Meta:

        db_table = "order_vip"
