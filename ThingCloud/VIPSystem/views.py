# -*- coding: utf-8 -*-
from django.shortcuts import render
from models import VIP
from OrderSystem.models import VIPOrder
from django.forms.models import model_to_dict
from TCD_lib.security import UserAuthorization
from TCD_lib.fee import getVIPfee
from datetime import datetime
import xml.etree.ElementTree as ET 
from TCD_lib.utils import Jsonify, dictPolish, unifyOrder, iosOrder, checkWechatOrder
import logging
logger = logging.getLogger('appserver')

# Create your views here.

@UserAuthorization
def vip(request):
    _user = request.user
    unfinishedOrder = VIPOrder.objects.filter(user_id=_user['uid']).filter(state=2)
    if unfinishedOrder:
        orderstate = 1
    else:
        orderstate = 0
    if not _user["vip"]:
        return Jsonify({"status":False, "state":False, error:"1501", "error_message":"用户还不是会员, 请先加入会员。", "processing":orderstate})
    _vip = VIP.objects.filter(vid=_user["vip"])
    if _vip:
        _vip = _vip[0]
        return Jsonify({"status":True, "state":True, error":"", "error_message":"", "processing":orderstate, "vip":dictPolish(model_to_dict(_vip)), "user":_user})
    else:
        return Jsonify({"status":False, "state":False, "error":"1501", "error_message":"用户还不是会员, 请先加入会员。", "processing":orderstate})

@UserAuthorization
def vipOrder(request):
    _user = request.user
    level=request.POST.get("level", 0)
    level = int(level)
    ipaddr = request.POST.get("ipaddr", "127.0.0.1")
    body = request.POST.get("body", "Unknown")
    detail = request.POST.get("detail", "Unknown")
    month = request.POST.get("month", None)
    if not month:
        return Jsonify({"status":False, "error":"1101", "error_message":u"输入信息不足。"})
    month = int(month)
    #fee = getVIPfee(month, level)
    fee=0.1
    ##Generate wechat preorder
    _order = VIPOrder(month=month, fee=fee, user_id=_user['uid'], level=level, state=0)
    _order.save()
    result = unifyOrder(model_to_dict(_order), body, detail, ipaddr, 1)
    fp = open("result.xml", "w+")
    fp.write(result)
    fp.close()
    prepayid = ""
    try:
        tree = ET.parse("result.xml")
        root = tree.getroot()
        if root[0].text == "SUCCESS":
            prepayid = root[8].text
        else:
            return Jsonify({"status":False, "error":"1310", "error_message":u"微信预支付失败，响应失败"})           
    except Exception, e:
        logger.error(e)
        logger.error("1311 wechat order failed")
        return Jsonify({"status":False, "error":"1311", "error_message":u"微信预支付失败, 未知错误。"})
    _order.prepayid = prepayid
    _order.save()
    #为iOS准备调起支付所需的参数
    data = iosOrder(prepayid)
    return Jsonify({"status":True, "error":"", "error_message":"", "order":model_to_dict(_order), "data":data})

@UserAuthorization
def vipConfirm(request):
    _user = request.user
    unfinishedOrder = VIPOrder.objects.filter(user_id=_user['uid']).filter(state=2)
    if unfinishedOrder:
        orderstate = 1
    else:
        orderstate = 0
    _vip = VIP.objects.filter(vid=_user["vip"])
    if _vip:
        _vip = model_to_dict(_vip[0])
        state = True
    else:
        state = False
        _vip = {}
    void = request.GET.get("void", None)
    if not void:
        return Jsonify({"status":False, "error":"1101", "error_message":u"输入信息不足。", "processing":orderstate, "vip":_vip, "state":state})
    _order = VIPOrder.objects.filter(void=void)
    if not _order:
        return Jsonify({"status":False, "error":"1502", "error_message":u"订单不存在。", "processing":orderstate, "vip":_vip, "state":state })
    _order = _order[0]
    orderState=_order.state
    if orderState == 1:
        return Jsonify({"status":True, "error":"", "error_message":u"", "processing":0, "vip":_vip, "state":state})
    else:
        result = checkWechatOrder(model_to_dict(_order), 1)

        #TODO: payState check
        fp = open("result.txt", "w+")
        fp.write(result)
        fp.close()

        payState = 0
        if payState == 0:
            _order.state=2
            _order.save()
            return Jsonify({"status":True, "error":"", "error_message":u"", "state":state, "vip":_vip, "processing":1})
        else:
            _order.state = 1
            _order.save()
            return Jsonify({"status":True, "error":"", "error_message":u"", "state":state, "vip":_vip, "processing":0})