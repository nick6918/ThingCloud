# -*- coding: utf-8 -*-

from django.shortcuts import render
from models import Feedback
from TCD_lib.utils import Jsonify
from TCD_lib.security import UserAuthorization
from django.forms.models import model_to_dict

# Create your views here.
@UserAuthorization
def feedback(request):
    _user = request.user
    notes = request.POST.get("notes", None)
    if not notes:
        return Jsonify({"status":False, "error":1101, "error_message":"信息不足, 请重新输入。"})
    fdback = Feedback(notes=notes, user_id=_user['uid'], state=0)
    fdback.save()
    return Jsonify({"status":True, "feedback":model_to_dict(fdback), "error":"", "error_message":""})

@UserAuthorization
def checkDiscount(request):
    _user = request.user
    discount = request.GET.get("discount", None)
    discount
    disc = Discount.objects.filter(showcode==discount).filter(state==1)
    if not disc:
        return Jsonify({"status":False, "error":1601, "error_message":"优惠码不存在或优惠已过期, 请关注其它活动。"})
    return Jsonify({"status":True, "error":"", "error_message":"恭喜, 奖品兑换成功。"})
