# -*- coding: utf-8 -*-

from django.db import models
from AccountSystem.models import User
from CloudList.models import Address, WareHouse
from WorkerSystem.models import Worker
from django.forms.models import model_to_dict
from TCD_lib.utils import dictPolish

# Create your models here.
class Courier(models.Model):
    crid = models.AutoField(primary_key=True)
    worker = models.OneToOneField(Worker)
    wh_belong = models.ForeignKey(WareHouse)

    class Meta:
        db_table = "work_courier"

class Order(models.Model):

    oid = models.AutoField(primary_key=True)
    addr = models.ForeignKey(Address, null=True, default=None)
    user = models.ForeignKey(User)
    notes = models.CharField(max_length=300)
    fee = models.FloatField()
    typeid = models.IntegerField()
    itemList = models.CharField(max_length=200)
    state = models.IntegerField()
    create_time = models.DateTimeField()
    paid_time = models.DateTimeField(null=True, default=None)
    finish_time = models.DateTimeField(null=True, default=None)
    prepayid = models.CharField(max_length=50)
    signature = models.CharField(max_length=50)
    showid = models.CharField(max_length=50)
    courier = models.ForeignKey(Courier, null=True, default=None)

    class Meta:

        db_table = "orders"

    def toDict(self):
        _order = model_to_dict(self)
        if self.courier:
            _order['courier_id'] = self.courier.employee.id
            _order['courier_name'] = self.courier.employee.name
        else:
            _order['courier_id'] = ""
            _order['courier_name'] = ""
        return dictPolish(_order)

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
    prepayid = models.CharField(max_length=50, null=True, default=None)
    fee = models.CharField(max_length=50)
    #state == 0, 未支付, state = 1, 已支付， state = 2， 支付处理中
    state = models.IntegerField()

    class Meta:

        db_table = "order_vip"

