# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.forms.models import model_to_dict
from models import Order, Complaint, VIPOrder
from CloudList.models import Thing
from AccountSystem.models import Address, User
from TCD_lib.security import UserAuthorization
from TCD_lib.fee import getDeliveryfee
from TCD_lib.utils import Jsonify, dictPolish, unifyOrder, iosOrder, checkWechatOrder, polish_address
from VIPSystem.models import VIP, VIPPackage
from datetime import datetime, timedelta
import random
import xml.etree.ElementTree as ET 
import logging
logger = logging.getLogger('appserver')

PAGECOUNT = 8
#PICURL = "http://staticimage.thingcloud.net/thingcloud-master.b0.upaiyun.com/"
PICURL = "http://staticimage.thingcloud.net/thingcloud/"
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def getThingList(itemList):
    thingList = []
    if itemList:
        print itemList
        itemList = itemList.split(",")
        for item in itemList:
            current_item = Thing.objects.filter(tid=item)
            if current_item:
                current_item = model_to_dict(current_item[0])
                if int(current_item['avatar'])==1:
                    current_item['avatarurl'] = PICURL+"thing/"+str(current_item['tid'])+".png"
                else:
                    current_item['avatarurl'] = PICURL+"thing/default.png"
                thingList.append(current_item)
    return thingList


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
        order = Order(user_id=_user['uid'], notes="", fee=0, typeid=typeid, itemList=itemlist, state=12, create_time=createtime, showid="0")
        order.save()
        newid = createtime.strftime("%Y%m%d")+"0"*(4-len(str(order.oid)))+str(order.oid)
        order.showid=newid
        order.save()
        return Jsonify({"status":True, "error":"", "error_message":"", "order":dictPolish(model_to_dict(order)), "address":""})
    else:
        _addr_object = _addr[0]
        _addr = model_to_dict(_addr_object)
     	fee, detail = getDeliveryfee(1)
        order = Order(user_id=_user['uid'], notes="", fee=fee, typeid=typeid, itemList=itemlist, state=12, create_time=createtime, addr=_addr_object)
        order.save()
        newid = createtime.strftime("%Y%m%d")+"0"*(4-len(str(order.oid)))+str(order.oid)
        order.showid=newid
        order.save()
        return Jsonify({"status":True, "error":"", "error_message":"", "order":dictPolish(model_to_dict(order)), "address":polish_address(_addr_object), "detail":detail})

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
        _order.fee=6
        _order.save()
        return Jsonify({"status":True, "error":"", "error_message":"", "order":dictPolish(model_to_dict(_order)), "detail":u"同仓存取快递费: 6元。"})

@UserAuthorization
def confirmOrder(request):
    oid = request.POST.get("oid", None)
    fee = request.POST.get("fee", None)
    notes = request.POST.get("notes", "")
    ipaddr = request.POST.get("ipaddr", "127.0.0.1")
    body = request.POST.get("body", "Unknown")
    detail = request.POST.get("detail", "Unknown")
    prepayid = request.POST.get("prepayid", None)
    if not fee or not oid:
        return Jsonify({"status":False, "error":"1101", "error_message":u"输入信息不足。"})
    oid = int(oid)
    fee = float(fee)
    _order = Order.objects.filter(oid=oid)
    if not _order:
        return Jsonify({"status":False, "error":"1302", "error_message":u"订单不存在。"})
    else:
        _order = _order[0]
        _sign = ""
        for i in range(8):
            _sign = _sign + ALPHABET[random.randint(0, 62)]
        _order.signature = _sign
        if notes:
            _order.notes = notes
        if fee != _order.fee:
            return Jsonify({"status":False, "error":"1303", "fee":fee, "order":dictPolish(model_to_dict(_order)), "error_message":u"订单价格有误， 请重新下单。"})
        ##wechat order
        if fee==0:
            _order.paid_time=datetime.now()
            _order.state=1
            _order.save()
            return Jsonify({"status":True, "error":"", "error_message":"", "order":dictPolish(model_to_dict(_order)), "detail":u"会员免运费: 0元。"})
        else:
            _order.state=0
            result = unifyOrder(model_to_dict(_order), body, detail, ipaddr, 0)
            if not prepayid:
                try:
                    root = ET.fromstring(result)
                    if root.find("return_code").text == "SUCCESS":
                        prepayid = root.find("prepay_id").text
                    else:
                        return Jsonify({"status":False, "error":"1310", "error_message":u"微信预支付失败，响应失败"})			
                    _order.prepayid = prepayid
                    _order.save()
                except Exception, e:
                    logger.error(e)
                    logger.error("1311 微信预支付失败， 未知错误")
                    return Jsonify({"status":False, "error":"1311", "error_message":u"微信预支付失败, 未知错误。"})
            #为iOS准备调起支付所需的参数
            data = iosOrder(prepayid)
            return Jsonify({"status":True, "error":"", "error_message":"", "order":dictPolish(model_to_dict(_order)), "data":data, "detail":u"同仓存取快递费: 6元。"})

# @UserAuthorization
# def checkPayment(request):
#     oid = request.GET.get("oid", None)
#     if not oid:
#         return Jsonify({"status":False, "error":"1101", "error_message":u"输入信息不足。"})
#     oid = int(oid)
#     _order = Order.objects.filter(oid=oid)
#     if not _order:
#         return Jsonify({"status":False, "error":"1302", "error_message":u"订单不存在。"})
#     else:
#         _order = _order[0]
#         state = _order.state
#         if state==1:
#             #支付成功， 且已经收到微信回调
#             return Jsonify({"status":True, "error":"", "error_message":"", "state":1})
#         else:
#             result = checkWechatOrder(model_to_dict(_order), 0)

#             #payState check
#             fp = open("result.txt", "w+")
#             fp.write(result)
#             fp.close()

#             #TODO: Analyse wechat check result
#             payState = 0
#             if payState:
#                 _order.state = 1
#                 _order.save()
#                 return Jsonify({"status":True, "error":"", "error_message":"", "state":1})
#             else:
#                 _order.state=2
#                 _order.save()
#                 return Jsonify({"status":True, "error":"", "error_message":"", "state":2})

@UserAuthorization
def getOrderList(request):
    typeid = request.GET.get("typeid", None)
    stateid = request.GET.get("stateid", None)
    page = request.GET.get("page", 0)
    page = int(page)
    _user = request.user
    resultList = []
    itemList = Order.objects.filter(user_id=_user['uid']).exclude(state=12).exclude(state=13).order_by('-oid')[PAGECOUNT*page:PAGECOUNT*(page+1)]
    if typeid:
        typeid=int(typeid)
        itemList = itemList.filter(typeid)
    if stateid:
        stateid=int(stateid)
        itemList = itemList.filter(stateid)
    for item in itemList:
        current_item = model_to_dict(item)
        current_address = Address.objects.filter(adid=item.addr_id)
        if current_address:
            current_address = current_address[0]
            current_item["address"]=polish_address(current_address)
        else:
            current_item["address"] = ""
        resultList.append(current_item)
    print resultList
    return Jsonify({"status":True, "error":"", "error_message":"", "orderlist":resultList})

@UserAuthorization
def getOrder(request):
    oid = request.GET.get("oid", None)
    checkPayment = request.GET.get("checkpayment", 0)
    checkPayment = int(checkPayment)
    _user = request.user
    if not oid:
        return Jsonify({"status":False, "error":"1101", "error_message":u"输入信息不足。"})
    oid = int(oid)
    _order = Order.objects.filter(oid=oid)
    if _order:
        _order = _order[0]
        if checkPayment==1 and int(_order.state)==0:
            result = checkWechatOrder(model_to_dict(_order), 0)

            payState = 0
            root = ET.fromstring(result)
            if root.find("return_code").text == "SUCCESS" and root.find("trade_state").text == "SUCCESS":
                payState = 1
            if payState == 1:
                _order.state =1
                _order.save()
            else:
                _order.state = 2
                _order.save()
        itemList = _order.itemList
        thingList = getThingList(itemList)
        address = Address.objects.filter(adid=_order.addr_id)
        if address:
            address=polish_address(address[0])
        else:
            address=""
        dictPolish(model_to_dict(_order))
        return Jsonify({"status":True, "error":"", "error_message":"", "order":dictPolish(model_to_dict(_order)), "address":address, "thinglist":thingList, "detail":u"同仓存取快递费: 6元。"})
    else:
        return Jsonify({"status":False, "error":"1302", "error_message":u"订单不存在。"})

@UserAuthorization
def cancel(request):
    oid = request.POST.get("oid", None)
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
            itemList = _order.itemList
            thingList = getThingList(itemList)
            address = Address.objects.filter(adid=_order.addr_id)
            if address:
                address=model_to_dict(address[0])
            else:
                address=""
            if _order.fee != 0:

                #微信退款
                #refundstate = Wechat.refund()
                refundstate=True

                if refundstate:
                    _order.state=8
                    _order.save()
                    return Jsonify({"status":True, "error":"", "error_message":"", "order":dictPolish(model_to_dict(_order)), "thinglist":thingList, "address":address, "detail":u"同仓存取快递费: 6元。"})
                else:
                    _order.save()
                    return Jsonify({"status":False, "error":"1304", "error_message":u"微信退款失败，请联系客服。"})
            else:
                _order.save()
                return Jsonify({"status":True, "error":"", "error_message":"", "order":dictPolish(model_to_dict(_order)), "thinglist":thingList, "address":address, "detail":u"同仓存取快递费: 6元。"})
        else:
            return Jsonify({"status":False, "error":"1303", "error_message":u"用户无权进行此操作。"})

@UserAuthorization
def complain(request):
    _user = request.user
    user = User.objects.filter(uid=user["uid"])
    user = user[0]
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
        if _order.state!=5:
            return Jsonify({"status":False, "error":"1303", "error_message":u"用户无权进行此操作。"})
        else:
            comp = Complaint(order_id=oid, user_id=_user["uid"], notes=notes, state=0)
            comp.save()
            _order.state = 9
            itemList = _order.itemList
            thingList = getThingList(itemList)
            address = Address.objects.filter(adid=_order.addr_id)
            if address:
                address=model_to_dict(address[0])
            else:
                address=""
            _order.save()
            return Jsonify({"status":True, "error":"", "error_message":"", "order":dictPolish(model_to_dict(_order)), "thinglist":thingList, "address":address, "detail":u"同仓存取快递费: 6元。"})

@UserAuthorization
def update(request):
    """
    Crucial interface.
    need user group check. @1: User @0:Engineer
    include PATH I：1(已支付)/2（支付处理中）->3(取/送件中)[->4（处理中)]->5(已送达)->6(已完成)
    include PATH II: 9(已申诉)->6(已完成)
    """

    #工程师， 一般用户， 管理员
    STATE_ALLOWED = [[1, 3, 4, 5, 9], [5,9], [1, 3, 4]]

    _user = request.user
    oid = request.POST.get("oid", None)
    origin = request.POST.get("origin", None)
    if not oid or not origin:
        return Jsonify({"status":False, "error":"1101", "error_message":u"输入信息不足。"})
    oid = int(oid)
    origin = int(origin)
    _order = Order.objects.filter(oid=oid)
    if not _order:
        return Jsonify({"status":False, "error":"1302", "error_message":u"订单不存在。"})
    _order = _order[0]
    thingList = getThingList(_order.itemList)
    address = Address.objects.filter(adid=_order.addr_id)
    if address:
        address=model_to_dict(address[0])
    else:
        address=""
    current_state=_order.state
    if origin!=current_state:
        return Jsonify({"status":False, "error":"1305", "error_message":u"订单状态不一致, 已重新刷新该订单。", "order":dictPolish(model_to_dict(_order)), "thinglist":thingList, "address":address})
    gid = _user['gid']
    if origin not in STATE_ALLOWED[gid]:
        return Jsonify({"status":False, "error":"1110", "error_message":u"用户无权进行此操作。"})
    state = 11
    if current_state == 1:
        _order.state = 3
    if current_state == 3:
        _order.state = 4
    if current_state == 4:
        _order.state = 5
    if current_state == 5 or current_state == 9:
        _order.state = 6
        _order.finish_time = datetime.now()
    _order.save()
    return Jsonify({"status":True, "error":"", "error_message":"", "order":dictPolish(model_to_dict(_order)), "thinglist":thingList, "address":address, "detail":u"同仓存取快递费: 6元。"})

@UserAuthorization
def delete(request):

    FINISH_STATE = [0, 6, 7, 8, 10, 11, 12]

    oid=request.POST.get("oid", None)
    _user = request.user
    if not oid:
        return Jsonify({"status":False, "error":"1101", "error_message":u"输入信息不足。"})
    oid = int(oid)
    _order = Order.objects.filter(oid=oid).filter(user_id=_user['uid'])
    if not _order:
        return Jsonify({"status":False, "error":"1110", "error_message":u"订单不存在或用户无权对此订单操作。"})
    _order = _order[0]
    if _order.state in FINISH_STATE:
        _order.state=13
        _order.save()
        return Jsonify({"status":True, "error":"", "error_message":""})
    else:
        return Jsonify({"status":False, "error":"1306", "error_message":u"订单正在处理中, 暂不能删除。 如遇特殊情况, 请直接联系客服。"})

def orderCallback(request):
    oid = request.POST.get("oid", None)
    _order = Order.objects.filter(oid=oid)
    if not oid:
        return Jsonify({"status":False, "error":"1101", "error_message":u"输入信息不足。"})
    if not _order:
        return Jsonify({"status":False, "error":"1302", "error_message":u"订单不存在。"})
    _order = _order[0]
    current_state = _order.state
    if current_state == 0 or current_state == 2:
        _order.state = 1
        _order.paid_time = datetime.now()
        _order.save()
        return Jsonify({"status":True, "error":"", "error_message":"", "order":dictPolish(model_to_dict(_order)), "detail":u"同仓存取快递费: 6元。"})
    else:
        return Jsonify({"status":False, "error":"1110", "order":dictPolish(model_to_dict(_order)),"detail":u"同仓存取快递费: 6元。", "error_message":u"用户无权进行此操作。"})

def vipCallback(request):
    void = request.GET.get("void", None)
    if not void:
        return Jsonify({"status":False, "error":"1101", "error_message":u"输入信息不足。"})
    void = int(void)
    viporder = VIPOrder.objects.filter(void=void)
    if not viporder:
        return Jsonify({"status":False, "error":"1502", "error_message":u"订单不存在。"})
    else:
        viporder = viporder[0]
        month = viporder.month
        _user = User.objects.filter(uid=viporder.user.uid)
        if not _user:
            return Jsonify({"status":False, "error":"1502", "error_message":u"该订单不属于任何用户。"})
        else:
            _user = _user[0]
            if not _user.vip:
                _vip = VIP()
                _vip.save()
                _user.vip=_vip
                _user.save()
            viporder.state=1
            viporder.save()
            newPackage = VIPPackage(level = viporder.level, days = viporder.month*31)
            _vip.addNewPackage(newPackage)
            return Jsonify({"status":True, "vip":_vip.toDict()})

