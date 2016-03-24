# -*- coding: utf-8 -*-
from django.shortcuts import render
from models import VIP
from OrderSystem.models import VIPOrder
from django.forms.models import model_to_dict
from TCD_lib.security import UserAuthorization
from datetime import datetime

def getFee(month, level):
    discount = 1
    base = 30
    if month >= 12:
        discount = 0.8
    fee = int(base * month * discount)
    return fee

# Create your views here.
@UserAuthorization
def vip(request):
    _user = request.user
    if not _user["vip_id"]:
        return Jsonify({"status":False, "error":"1501", "error_message":"用户还不是会员, 请先加入会员。"})
    _vip = VIP.objects.filter(vid=_user["vip_id"])
    if _vip:
        _vip = _vip[0]
        return Jsonify({"status":True, "error":"", "error_message":"", "vip":model_to_dict(_vip)})
    else:
        return Jsonify({"status":False, "error":"1501", "error_message":"用户还不是会员, 请先加入会员。"})

@UserAuthorization
def vipOrder(request):
    _user = request.user
    level=request.POST.get("level", 0)
    level = int(level)
    month = request.POST.get("month", None)
    if not month:
        return Jsonify({"status":False, "error":"1101", "error_message":u"输入信息不足。"})
    month = int(month)
    fee = getFee(month, level)
    ##Generate wechat preorder
    ##TODO
    prepayid = 123456
    ##Generate new vip order
    _order = VIPOrder(month=month, fee=fee, prepayid=prepayid, user=_user, level=level, state=0)
    _order.save()
    return Jsonify({"status":True, "error":"", "error_message":"", "order":model_to_dict(_order)})

@UserAuthorization
def vipConfirm(request):
    _user = request.user
    void = request.GET.get("void", None)
    if not void:
        return Jsonify({"status":False, "error":"1101", "error_message":u"输入信息不足。"})
    _order = VIPOrder.objects.filter(void=void)
    if not _order:
        return Jsonify({"status":False, "error":"1502", "error_message":u"订单不存在。"})
    _order = _order[0]
    state=_order.state
    if state==0:
        _order.state=2
        _order.save()
        return Jsonify({"status":True, "error":"", "error_message":u"", "state":2})
    else:
        _vip = VIP.objects.filter(vid=_user['vip_id'])
        if not _vip:
            return Jsonify({"status":False, "error":"1501", "error_message":"用户还不是会员, 请先加入会员。"})
        _vip = _vip[0]
        return Jsonify({"status":True, "error":"", "error_message":u"", "state":state, "vip":model_to_dict(_vip)})

def vipCallback(request):
    void = request.POST.get("void", None)
    if not void:
        return Jsonify({"status":False, "error":"1101", "error_message":u"输入信息不足。"})
    void = int(void)
    viporder = VIPOrder.objects.filter(void=void)
    if not viporder:
        return Jsonify({"status":False, "error":"1502", "error_message":u"订单不存在。"})
    else:
        viporder = viporder[0]
        month = viporder.month
        _user = User.objects.filter(uid=viporder.user_id)
        if not _user:
            return Jsonify({"status":False, "error":"1502", "error_message":u"该订单不属于任何用户。"})
        else:
            _user = _user[0]
            _vip = _user.vip
            if not _vip:
                _vip = VIP(start_date=datetime.now(), end_date=datetime.now()+timedelta(31*month), level=0)
                _vip.save()
                return Jsonify({"status":True, "vip":model_to_dict(_vip)})
            else:
                enddate = _vip.end_date
                newend = enddate + timedelta(31*month)
                _vip.end_date = newend
                _vip.save()
                return Jsonify({"status":True, "vip":model_to_dict(_vip)})
