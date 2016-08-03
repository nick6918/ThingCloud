# -*- coding: utf-8 -*-

from django.db import models
from AccountSystem.models import User
from CloudList.models import Address, WareHouse, Thing
from WorkerSystem.models import Worker
from django.forms.models import model_to_dict
from TCD_lib.utils import dictPolish
from TCD_lib.picture import Files
from TCD_lib.settings import PICURL, UPYUNURL
from TCD_lib.business import generateInfo, html_head, html_tail

FILEPATH = UPYUNURL+u"/orderfiles/"

import logging
logger = logging.getLogger('appserver')

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

    def flushInfo(self):
        infoList = html_head + generateInfo(self, self.state) + html_tail
        # fp = open("./htmltext/"+str(self.oid)+".html", "w+")
        # fp.write(infoList.encode('UTF-8'))
        # fp.close()
        # status = True
        try:
            status = Files().uploadFiles("thingcloud/htmltext/"+ str(self.oid) + ".html", infoList.encode('UTF-8'))
        except Exception, e:
            logger.error(e)
        if not status:
            logger.error("1415, HTML UPLOAD ERROR")
        return status

    def toDict(self):
        _order = model_to_dict(self)
        #_order["texturl"] = "testapi.thingcloud.net:8001/htmltext?oid"+ str(self.oid) + ".html"
        _order["texturl"] = "staticimage.thingcloud.net/thingcloud/htmltext/" + str(self.oid) + ".html"
        _order["total_units"] = self.getTotalUnits()
        return dictPolish(_order)

    def getThingList(self):
        thingList = []
        itemList = self.itemList.split(",")
        for item in itemList:
            if item:
                current_item = Thing.objects.filter(tid=item)
                if current_item:
                    current_item = current_item[0].toDict()
                    thingList.append(current_item)
        return thingList

    def getTotalUnits(self):
        total_units = 0
        itemList = self.itemList.split(",")
        for item in itemList:
            if item:
                thing = Thing.objects.filter(tid=item)
                if thing:
                    thing = thing[0]
                    total_units += thing.units
        return total_units

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

