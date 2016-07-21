# -*- coding: utf-8 -*-
from django.shortcuts import render
from models import VIP, VIPPackage
from AccountSystem.models import User
from OrderSystem.models import VIPOrder
from django.forms.models import model_to_dict
from TCD_lib.security import UserAuthorization
from TCD_lib.fee import getVIPfee
from datetime import datetime, timedelta
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
        return Jsonify({"status":False, "state":False, "error":"1501", "error_message":"用户还不是会员, 请先加入会员。", "processing":orderstate})
    _vip = VIP.objects.filter(vid=_user["vip"])
    if _vip:
        _vip = _vip[0]
        _vip.flush()
        return Jsonify({"status":True, "state":True, "error":"", "error_message":"", "processing":orderstate, "vip":_vip.toDict(), "user":_user})
    else:
        return Jsonify({"status":False, "state":False, "error":"1501", "error_message":"用户还不是会员, 请先加入会员。", "processing":orderstate})

@UserAuthorization
def vipOrder(request):
    _user = request.user
    ipaddr = request.POST.get("ipaddr", "127.0.0.1")
    typeid = request.POST.get("typeid", None)
    fee = request.POST.get("fee", None)
    body = request.POST.get("body", "Unknown")
    detail = request.POST.get("detail", "Unknown")
    month = request.POST.get("month", None)
    if not month or not typeid or not fee:
        return Jsonify({"status":False, "error":"1101", "error_message":u"输入信息不足。"})
    fee = float(fee)
    month = int(month)
    typeid = int(typeid)
    server_fee = getVIPfee(month, typeid, typeid)
    if fee != server_fee:
        return Jsonify({"status":False, "error":"1510", "error_message":u"费用有误，您的订单费用为"+str(server_fee)+u"元。", "fee":server_fee})
    ##Generate wechat preorder
    _order = VIPOrder(month=month, fee=fee, user_id=_user['uid'], level=typeid, state=0)
    _order.save()
    result = unifyOrder(model_to_dict(_order), body, detail, ipaddr, 1)
    prepayid = ""
    try:
        root = ET.fromstring(result)
        if root.find("return_code").text == "SUCCESS":
            prepayid = root.find("prepay_id").text
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
    _vip = VIP.objects.filter(vid=_user["vip"])
    if _vip:
        _vip = _vip[0]
        _vip.flush()
        vip_info = _vip.toDict()
    else:
        _vip = None
        vip_info = {}
    has_processing_order = False
    unfinishedOrder = VIPOrder.objects.filter(user_id=_user['uid']).filter(state=2)
    if unfinishedOrder:
        has_processing_order = True
    void = request.GET.get("void", None)
    if not void:
        return Jsonify({"status":False, "error":"1101", "error_message":u"输入信息不足。", "processing":has_processing_order, "vip":vip_info, "state":bool(vip_info)})
    _order = VIPOrder.objects.filter(void=void)
    if not _order:
        return Jsonify({"status":False, "error":"1502", "error_message":u"订单不存在。", "processing":has_processing_order, "vip":vip_info, "state":bool(vip_info)})
    _order = _order[0]
    if _order.state == 1:
        return Jsonify({"status":True, "error":"", "error_message":u"", "processing":0, "vip":vip_info, "state":bool(vip_info)})
    else:
        result = checkWechatOrder(model_to_dict(_order), 1)
        try:
            root = ET.fromstring(result)
            if root.find("return_code").text == "SUCCESS" and root.find("trade_state").text == "SUCCESS":
                _order.state = 1
                _order.save()
                newPackage = VIPPackage(level = _order.level, days = _order.month*31)
                if not _vip:
                    _vip = VIP()
                    user = User.objects.filter(uid=_user["uid"])[0]
                    user.vip = _vip
                    user.save()
                _vip.addNewPackage(newPackage)
                vip_info = _vip.toDict()
                return Jsonify({"status":True, "error":"", "error_message":u"", "state":bool(vip_info), "vip":vip_info, "processing":0})
            else:
                _order.state=2
                _order.save()
                return Jsonify({"status":True, "error":"", "error_message":u"", "state":bool(vip_info), "vip":vip_info, "processing":1})
        except Exception, e:
            logger.error(e)
            return Jsonify({"status":False, "error":"1512", "error_message":u"微信查询失败。", "processing":1, "vip":vip_info, "state":bool(vip_info)})