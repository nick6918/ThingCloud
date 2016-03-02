# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.forms.models import model_to_dict
from models import Order, Complaint
from AccountSystem.models import Address
from TCD_lib.security import UserAuthorization
from TCD_lib.utils import Jsonify
from datetime import datetime

@UserAuthorization
def generateOrder(request):
    _user = request.user
    typeid = request.POST.get("typeid", None)
    if not typeid:
        return Jsonify({"status":False, "error":"1101", "error_message":u"输入信息不足。"})
    typeid = int(typeid)
    #itemlist is a list of item number, eg.
    #"1101, 1302, 1323, 1333"
    itemlist = request.POST.get("itemlist", "")
    createtime = datetime.now()
    _user = request.user
    _addr = Address.objects.filter(user_id=_user['uid']).filter(is_default=1)
    if not _addr:
        order = Order(user_id=_user['uid'], notes="", fee=0, typeid=typeid, itemList=itemlist, state=0, create_time=createtime)
        order.save()
        return Jsonify({"status":True, "error":"", "error_message":"", "order":order, "address":""})
    else:
        _addr_object = _addr[0]
        _addr = model_to_dict(_addr_object)
        order = Order(user_id=_user['uid'], notes="", fee=6, typeid=typeid, itemList=itemlist, state=0, create_time=createtime, addr=_addr_object)
        order.save()
        return Jsonify({"status":True, "error":"", "error_message":"", "order":model_to_dict(order), "address":{"name":_addr["name"], "gender":_addr["gender"], "address":_addr["addr"], "phone":_addr["phone"]},})

@UserAuthorization
def modifyOrder(request):
    oid = request.POST.get("oid", None)
    addrid = request.POST.get("addrid", None)
    if not oid or not addrid:
        return Jsonify({"status":False, "error":"1101", "error_message":u"输入信息不足。"})
    oid = int(oid)
    addrid = int(addrid)
    _order = Order.objects.filter(oid=oid)
    if not _order:
        return Jsonify({"status":False, "error":"1302", "error_message":u"订单不存在。"})
    else:
        _order = _order[0]
        _order.addr_id = addrid
        _order.save()
        return Jsonify({"status":True, "error":"", "error_message":"", "order":model_to_dict(_order)})

@UserAuthorization
def confirmOrder(request):
    oid = request.POST.get("oid", None)
    fee = request.POST.get("fee", None)
    notes = request.POST.get("notes", "")
    if not fee or not oid:
        return Jsonify({"status":False, "error":"1101", "error_message":u"输入信息不足。"})
    oid = int(oid)
    fee = int(fee)
    _order = Order.objects.filter(oid=oid)
    if not _order:
        return Jsonify({"status":False, "error":"1302", "error_message":u"订单不存在。"})
    else:
        _order = _order[0]
        if notes:
            _order.notes = notes
        if fee != _order.fee:
            return Jsonify({"status":False, "error":"1303", "error_message":u"订单价格有误， 请重新下单。"})
        ##wechat order
        if fee==0:
            _order.paytime=datetime.now()
            _order.state=1
            _order.save()
            return Jsonify({"status":True, "error":"", "error_message":"", "order":model_to_dict(_order)})
        else:
            #申请微信订单
            prepayid=10001
            _order.prepayid = prepayid
            _order.save()
            return Jsonify({"status":True, "error":"", "error_message":"", "order":model_to_dict(_order)})

@UserAuthorization
def checkPayment(request):
    oid = request.GET.get("oid", None)
    if not oid:
        return Jsonify({"status":False, "error":"1101", "error_message":u"输入信息不足。"})
    oid = int(oid)
    _order = Order.objects.filter(oid=oid)
    if not _order:
        return Jsonify({"status":False, "error":"1302", "error_message":u"订单不存在。"})
    else:
        _order = _order[0]
        state = _order.state
        if state==1:
            return Jsonify({"status":True, "error":"", "error_message":"", "state":1})
        else:
            _order.state=2
            _order.save()
            return Jsonify({"status":True, "error":"", "error_message":"", "state":2})

@UserAuthorization
def getOrderList(request):
    typeid = request.GET.get("typeid", None)
    stateid = request.GET.get("stateid", None)
    _user = request.user
    resultList = []
    itemList = Order.objects.filter(user_id=_user['uid'])
    if typeid:
        typeid=int(typeid)
        itemList = itemList.filter(typeid)
    if stateid:
        stateid=int(stateid)
        itemList = itemList.filter(stateid)
    for item in itemList:
        resultList.append(model_to_dict(item))
    print resultList
    return Jsonify({"status":True, "error":"", "error_message":"", "orderlist":resultList})

@UserAuthorization
def cancel(request):
    oid = request.GET.get("oid", None)
    if not oid:
        return Jsonify({"status":False, "error":"1101", "error_message":u"输入信息不足。"})
    oid = int(oid)
    _order = Order.objects.filter(oid=oid)
    if not _order:
        return Jsonify({"status":False, "error":"1302", "error_message":u"订单不存在。"})
    else:
        _order = _order[0]
        state = _order.state
        if state <= 2:
            _order.state = 7
            if _order.fee != 0:

                #微信退款
                #refundstate = Wechat.refund()
                refundstate=True

                if refundstate:
                    _order.state=8
                    _order.save()
                    return Jsonify({"status":True, "error":"", "error_message":"", "state":8})
                else:
                    _order.save()
                    return Jsonify({"status":False, "error":"1304", "error_message":u"微信退款失败，请联系客服。"})
            else:
                _order.save()
                return Jsonify({"status":True, "error":"", "error_message":"", "state":7})
        else:
            return Jsonify({"status":False, "error":"1303", "error_message":u"用户无权进行此操作。"})

@UserAuthorization
def complain(request):
    _user = request.user
    oid = request.POST.get("oid", None)
    notes = request.POST.get("notes", None)
    if not oid or not notes:
        return Jsonify({"status":False, "error":"1101", "error_message":u"输入信息不足。"})
    oid = int(oid)
    _order = Order.objects.filter(oid=oid)
    if not _order:
        return Jsonify({"status":False, "error":"1302", "error_message":u"订单不存在。"})
    else:
        _order = _order[0]
        if _order.state!=6:
            return Jsonify({"status":False, "error":"1303", "error_message":u"用户无权进行此操作。"})
        else:
            comp = Complaint(order_id=oid, user_id=_user["uid"], notes=notes, state=0)
            comp.save()
            _order.state = 9
            _order.save()
            return Jsonify({"status":True, "error":"", "error_message":"", "state":9})
