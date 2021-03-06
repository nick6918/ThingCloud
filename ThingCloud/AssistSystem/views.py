# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from models import Feedback, Discount, Activity, Version
from CloudList.models import Community
from TCD_lib.utils import Jsonify
from TCD_lib.fee import feeList
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
    discount = discount.upper()
    disc = Discount.objects.filter(showcode=discount).filter(state=1)
    if not disc:
        return Jsonify({"status":False, "error":1601, "error_message":"优惠码不存在或优惠已过期, 请关注其它活动。"})
    disc = disc[0]
    return Jsonify({"status":True, "error":"", "error_message":disc.message})

def activityList(request):
    activities = Activity.objects.filter(state=1).order_by('-priority', '-acid')
    resultList = []
    for activity in activities:
        resultList.append(model_to_dict(activity))
    return Jsonify({"status":True, "error":"", "activittlist":resultList})

def versionInfo(request):
    typeid = 0
    machine = request.GET.get("machine", "others")
    #machine = unicode(machine)
    if machine.upper() == "ANDROID":
        typeid = 1
    elif machine.upper() == "WEB":
        typeid = 2
    elif machine.upper() == "IOS":
        typeid = 0
    else:
        typeid = 3
    version = Version.objects.filter(typeid=typeid).filter(state__gt=0).order_by('-vrid')
    if version:
        version = version[0]
        keylist = {}
        if version.compulsorylist:
            for item in version.compulsorylist.strip(" ").split(","):
                keylist[item] = "F"
        if version.selectlist:
            for item in version.selectlist.strip(" ").split(","):
                keylist[item] = "S"
        _version = model_to_dict(version)
        del _version["compulsorylist"]
        del _version["selectlist"]
        _version["versionlist"] = keylist   
        return Jsonify({"status":True, "error":"", "version":_version})
    else:
        return Jsonify({"status":False, "error":1602, "error_message":"当前系统无可用版本。"})

def communityList(request):
    result = {}
    for item in Community.objects.filter(state=1):
        district = item.district_belong
        city = district.city_belong
        if city.name in result.keys():
            if district.name in result[city.name][1].keys():
                result[city.name][1][district.name][1].append(model_to_dict(item))
            else:
                meta_district = model_to_dict(district)
                result[city.name][1][district.name] = [meta_district, [model_to_dict(item), ]]
        else:
            meta_city = model_to_dict(city)
            meta_district = model_to_dict(district)
            result[city.name] = [meta_city, {district.name: [meta_district, [model_to_dict(item), ]], }]
    return Jsonify({"status":True, "error":"", "data":result})

def getFeeList(request):
    origin, current, discount = feeList()
    return Jsonify({"status":True, "error":"", "origin":origin, "current":current, "discount":discount})

def joinUs(request):
    fp = open("TCD_lib/resources/join.html", "r")
    context = fp.read()
    httpResponse = HttpResponse(context, content_type="text/html")
    return httpResponse
