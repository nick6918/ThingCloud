# -*- coding: utf-8 -*-

from django.shortcuts import render
from datetime import datetime
from django.forms.models import model_to_dict
from models import Thing
from TCD_lib.security import UserAuthorization
from TCD_lib.utils import Jsonify
from TCD_lib.constants import TYPECONSTANT, PAGECOUNT
from TCD_lib.picture import Picture, UPYUNURL

AVATARPATH = UPYUNURL+"/thingavatar/"

# Create your views here.
def addNewItem(request):
    character = request.POST.get("character", u'未知')
    timeAdd = datetime.now()
    typeid = request.POST.get("typeid", 7)
    typeid = int(typeid)
    gender = request.POST.get("gender", 2)
    gender = int(gender)
    avatar = request.FILES.get("avatar", None)
    if avatar:
        _hasAvatar = 1
    else:
        _hasAvatar = 0
    subtype_name = request.POST.get("subname", u"未知")
    user_belong_to_id = request.POST.get("uid", None)
    wh_in_id = request.POST.get("whid", None)
    _name = TYPECONSTANT[typeid] + "-" + subtype_name + "-" + character
    if not user_belong_to_id or not wh_in_id:
        return Jsonify({"status":False, "error":1101, "error_message":"信息不足, 请输入用户id以及仓库id。"})
    thing = Thing(avatar=_hasAvatar, name=_name, time_saved=timeAdd, typeid=typeid, gender=gender, subtype_name= subtype_name, user_belong_to_id= user_belong_to_id, wh_in_id=wh_in_id, state=1)
    thing.save()
    _tid = thing.tid
    thing = model_to_dict(thing)
    del(thing['time_saved'])
    del(thing['state'])
    del(thing['user_belong_to'])
    if False:
		currentPath = AVATARPATH + str(_tid) + ".png"
		data = ""
		for chunk in avatar.chunks():
			data += chunk
		try:
			state = Picture().uploadPicture(currentPath, data)
			if state:
				return Jsonify({"status":True, "error":"", "error_message":"", "tid":_tid})
			else:
				logger.error("1109 UPYUN UPLOAD FAILED")
				try:
					_user = User.objects.get(uid=user['uid'])
					_user.avatar = False
					_user.save()
				except Exception,e:
					logger.error(e)
					logger.error("1109 User Acquirement Fail")
			return Jsonify({"status":False, "error":"1109", "error_message":"图片上传失败, 使用默认图片。", "thing":thing})
		except Exception, e:
			logger.error("upload error")
			logger.error(e)
			return Jsonify({"status":False, "error":"1109", "error_message":"图片上传失败, 使用默认图片。"})
    return Jsonify({"status":True, "thing":thing, "error":"", "error_message":""})

@UserAuthorization
def modifyNotes(request):
    _notes = request.POST.get("notes", None)
    tid = request.POST.get("tid", None)
    _user = request.user
    if not _notes or not tid:
        return Jsonify({"status":False, "error":1101, "error_message":"信息不足, 请输入备注。"})
    else:
        thing = Thing.objects.filter(user_belong_to_id=_user['uid']).filter(tid=tid)
        if thing:
            thing = thing[0]
            thing.notes=_notes
            thing.save()
        else:
            return Jsonify({"status":False, "error":1201, "error_message":"商品不存在。"})
    return Jsonify({"status":True, "error":"", "error_message":""})



@UserAuthorization
def getItemList(request):
    #can only get one type of item
    typeid = request.GET.get("typeid", None)
    page = request.GET.get("page", 0)
    page = int(page)
    user = request.user
    print user['uid']
    if typeid:
        typeid = int(typeid)
        itemList = Thing.objects.filter(user_belong_to_id=user['uid']).filter(state=1).filter(typeid=typeid)[PAGECOUNT*page:PAGECOUNT*(page+1)]
    else:
        itemList = Thing.objects.filter(user_belong_to_id=user['uid']).filter(state=1)[PAGECOUNT*page:PAGECOUNT*(page+1)]
    resultList = []
    if itemList:
        for item in itemList:
            wh_id = item.wh_in.wid
            wh_name = item.wh_in.name
            item = model_to_dict(item)
            item['wh_id']=wh_id
            item['wh_name']=wh_name
            del(item['wh_in'])
            del(item['user_belong_to'])
            del(item['time_saved'])
            del(item['state'])
            resultList.append(item)
    return Jsonify({"status":True, "itemlist":resultList, "error":"", "error_message":""})
