# -*- coding: utf-8 -*-

from django.shortcuts import render
from datetime import datetime
from models import Thing
from TCD_lib.security import UserAuthorization
from TCD_lib.utils import Jsonify

# Create your views here.
def addNewItem(request):
    _name = request.POST.get("name", u'未知')
    timeAdd = datetime.now()
    typeid = request.POST.get("typeid", 6)
    typeid = int(typeid)
    gender = request.POST.get("gender", 2)
    gender = int(gender)
    subtype_name = request.POST.get("subname", None)
    user_belong_to_id = request.POST.get("uid", None)
    if not user_belong_to_id:
        return Jsonify({"status":False, "error":1103, "error_message":"Not enough message"})
    wh_in_id = request.POST.get("whid", None)
    thing = Thing(name=_name, time_saved=timeAdd, typeid=typeid, gender=gender, subtype_name= subtype_name, user_belong_to_id= user_belong_to_id, wh_in_id=wh_in_id)
    thing.save()
    print thing
    return Jsonify({"status":True, "thing":thing})

@UserAuthorization
def modifyNotes(request):
    notes = request.POST.get("notes", None)
    tid = request.POST.get("tid", None)
    _user = request.user
    if not notes or not tid:
        return Jsonify({"status":False, "error":1103, "error_message":"Not enough message"})
    else:
        thing = Thing.objects.filter(uid=_user['uid']).filter(tid=tid)
        thing['notes']=notes
        thing.save()
        print thing
    return Jsonify({"status":True})



@UserAuthorization
def getItemList(request):
    #can only get one type of item
    typeid = request.POST.GET("typeid", None)
    user = request.user
    itemList = Thing.objects.filter(uid=user['uid'])
    if typeid:
        itemlist = itemList.filter(typeid=typeid)
    return Jsonify({"status":True, "itemlist":itemList})
