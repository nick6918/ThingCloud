# -*- coding: utf-8 -*-
from django.shortcuts import render
from models import VIP
from django.forms.models import model_to_dict

# Create your views here.
def vip(request):
    _user = request.user
    print _user
    if not _user["vip_id"]:
        return Jsonify({"status":False, "error":"1501", "error_message":"用户还不是会员, 请先加入会员。"})
    # if request.method == 'GET':
    #     _vip = VIP.objects.filter(vid=_user["vip_id"])
    #     return Jsonify({"status":True, "error":"", "error_message":"", "vip":model_to_dict(_vip)})
    # else:
    return Jsonify({"status":False, "error":"1502", "error_message":"尚未实现。"})
