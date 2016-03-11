# -*- coding: utf-8 -*-
from TCD_lib.picture import Picture
from TCD_lib.settings import UPYUNURL, image_user, image_password, image_bucket
from django.shortcuts import render

from django.forms.models import model_to_dict
from datetime import datetime
from TCD_lib.utils import get_client_ip, Jsonify
from TCD_lib.security import Salt
from TCD_lib.picture import Picture
from models import User, UserSession, Code, Address
import time,math, logging, random
from TCD_lib.security import UserAuthorization
logger = logging.getLogger('appserver')

# Create your views here.
#UPYUNURL = "http://staticimage.thingcloud.net"
AVATARPATH = UPYUNURL+"/avatar/"

def createSession(user):
	salt = Salt()
	timestamp = str(int(math.floor(time.time())))
	sessionPassword = salt.hash(str(user['uid'])+"|"+timestamp)
	session = UserSession(uid = user['uid'], session_password = sessionPassword)
	session.save()
	return sessionPassword

def updateSession(user):
	session = UserSession.objects.filter(uid=user['uid'])
	if session:
		session = session[0]
		salt = Salt()
		timestamp = str(int(math.floor(time.time())))
		sessionPassword = salt.hash(str(user['uid'])+"|"+timestamp)
		session.session_password = sessionPassword
		session.save()
		return sessionPassword
	else:
		return createSession(user)

def register(request):
	"""
	Interface that allows user to register using phone number.
	Parameters:
		@request: Http Request.
	Returns:
		@result: Http Response in JSON.
	"""
	user = {"gid" : 1, "version": "1.0 User"}
	user['phone'] = request.POST.get("phone", None)
	user['nickname'] = request.POST.get("nickname", None)
	user['password'] = request.POST.get("password", None)
	gid = request.POST.get("gid", None)
	if gid:
		user['gid']=gid
	if not (user['nickname'] and user['password'] and user['phone']):
		return Jsonify({"status":False, "error":"1101", "error_message":"信息不足, 请重新输入。"})
	userList = User.objects.filter(nickname = user['nickname'])
	if userList:
		return Jsonify({"status":False, "error":"1108", "error_message":"昵称已被注册, 请重新输入。"})
	userList = User.objects.filter(phone=user['phone'])
	if userList:
		return Jsonify({"status":False, "error":"1105", "error_message":"手机号已注册, 请直接登录。"})
	user['loginIp'] = get_client_ip(request)
	user['registerTime'] = datetime.now()
	user['birthday'] = request.POST.get("birthday", "")
	gender = request.POST.get("gender", 2)
	user['gender'] = int(gender)
	avatar = request.FILES.get("avatar", None)
	if avatar:
		user['hasAvatar'] = 1
		#Upload the avatar here.
	else:
		user['hasAvatar'] = 0
	salt = Salt()
	#username在注册时确定， 此后不再改变。
	user['username'] = "USER"+salt.generateSalt(10) +"@sharecloud.com"
	timestamp = str(int(math.floor(time.time())))
	_hash = salt.hash(salt.md5(user['password']) + "|" + user['username'] + "|" + timestamp)
	password = salt.md5(_hash+salt.md5(user['password']))
	currentUser = User(gid = user["gid"], phone=user['phone'],nickname = user['nickname'], gender = user['gender'], birthday = user['birthday'], register = user['registerTime'], lastLogin = user['registerTime'], loginIp = user['loginIp'], avatar = user['hasAvatar'], salt = _hash, password = password, username = user['username'] )
	currentUser.save()
	user['uid'] = currentUser.uid
	user['session'] = createSession(user)
	if False:
		currentPath = AVATARPATH + str(user['uid']) + ".png"
		data = ""
		for chunk in avatar.chunks():
			data += chunk
		try:
			state = Picture().uploadPicture(currentPath, data)
			if state:
				return Jsonify({"status":True, "error":"", "error_message":"", "user":user})
			else:
				logger.error("1109 UPYUN UPLOAD FAILED")
				try:
					_user = User.objects.get(uid=user['uid'])
					_user.avatar = False
					_user.save()
				except Exception,e:
					logger.error(e)
					logger.error("1109 User Acquirement Fail")
			return Jsonify({"status":False, "error":"1109", "error_message":"图片上传失败, 使用默认图片。", "user":user})
		except Exception, e:
			logger.error("upload error")
			logger.error(e)
			return Jsonify({"status":False, "error":"1109", "error_message":"图片上传失败, 使用默认图片。"})
	del(user['registerTime'])
	del(user['loginIp'])
	del(user['password'])
	return Jsonify({"status":True, "error":"", "error_message":"", "user":user})

def sendCode(request):
	"""
		Generate and save code, send by message to user.
		This code can never be sent or saved by client.
	"""
	phone = request.GET.get("phone", None)
	if not phone:
		return Jsonify({"status":False, "error":"1101", "error_message":"信息不足, 请输入手机号"})
	phone=int(phone)
	user = User.objects.filter(phone=phone)
	if user:
		return Jsonify({"status":False, "error":"1105", "error_message":"手机号已注册, 请直接登录"})
	else:
		#code = random.randint(100000, 1000000)
		code = 123456
		current_code = Code.objects.filter(phone=phone)
		if current_code:
			current_code=current_code[0]
			current_code.code=code
		else:
			current_code = Code(phone=phone, code=code)
		current_code.save()
		#iMessage.send(phone, code)
		return Jsonify({"status":True, "error":"", "error_message":"", "message":True})

def checkCode(request):
	_code = request.GET.get('code', None)
	_phone = request.GET.get('phone', None)
	if not _code or not _phone:
		return Jsonify({"status":False, "error":"1101", "error_message":"信息不足, 请输入验证码。"})
	code = Code.objects.filter(phone=_phone)
	if not code or (_code != unicode(code[0].code)):
		return Jsonify({"status":False, "error":"1104", "error_message":"验证码输入有误, 请重新输入。"})
	return Jsonify({"status":True, "wait":1, "error":"", "error_message":""})

def loginByPhone(request):
	"""
	login by phone, return dynamic session.
	"""
	phone = request.POST.get('phone', None)
	user_password = request.POST.get('password', None)
	if not (phone and user_password):
		return Jsonify({"status":False, "error":"1101", "error_message":"信息不足, 请输入手机号和密码"})
	user = User.objects.filter(phone = phone)
	salt = Salt()
	if not user:
		return Jsonify({"status":False, "error":"1107", "error_message":"手机号未注册, 请首先注册。"})
	user = model_to_dict(user[0])
	if user['password'] == salt.md5(user['salt']+salt.md5(user_password)):
		user['session'] = updateSession(user)
		#some info is not allowed to be known by clients
		del user['salt']
		del user['password']
		del user['register']
		del user['loginIp']
		del user['lastLogin']
		return Jsonify({"status":True, "error":"", "error_message":"", "user":user})
	else:
		return Jsonify({"status":False, "error":"1106", "error_message":"密码有误, 请重新输入"})

@UserAuthorization
def address(request):
	_user = request.user
	if request.method == 'POST':
		addr = request.POST.get("addr", None)
		name = request.POST.get("name", None)
		gender = request.POST.get("gender", None)
		phone = request.POST.get("phone", None)
		tag = request.POST.get("tag", None)
		is_default = request.POST.get("isdefault", 0)
		addrid = request.POST.get("addrid", None)
		def_address = Address.objects.filter(user_id=_user['uid']).filter(is_default=1)
		if def_address:
			def_address = def_address[0]
		else:
			def_address = None
		if not addrid:
			#生成新的地址信息
			if not addr or not name or not gender or not phone:
				return Jsonify({"status":False, "error":"1101", "error_message":"信息不足。"})
			if not def_address:
				is_default=1
			address = Address(phone=phone, addr=addr, name=name, gender=gender, is_default=is_default, user_id=_user['uid'])
			if tag:
				address.tagid = tag
			address.save()
		else:
			#修改id为addrid的地址的部分信息
			address = Address.objects.filter(adid=addrid)
			if not address:
				return Jsonify({"status":False, "error":"1111", "error_message":"地址不存在。"})
			else:
				address = address[0]
				if phone:
					address.phone = phone
				if name:
					address.name = name
				if gender:
					address.gender = gender
				if tag:
					address.tag = tag
				if addr:
					address.addr = addr
				if is_default=="1":
					def_address.is_default=0
					def_address.save()
					address.is_default=1
				address.save()
		return Jsonify({"status":True, "error":"", "error_message":"", "address":model_to_dict(address)})
	if request.method == 'GET':
		addrid = request.GET.get("addrid")
		if not addrid:
			return Jsonify({"status":False, "error":"1101", "error_message":"信息不足。"})
		else:
			addrid = int(addrid)
			address = Address.objects.filter(adid=addrid)
			if not address:
				return Jsonify({"status":False, "error":"1111", "error_message":"地址不存在。"})
			else:
				address = address[0]
				return Jsonify({"status":True, "error":"", "error_message":"", "address":model_to_dict(address)})

@UserAuthorization
def addressList(request):
	_user = request.user
	addressList = Address.objects.filter(user_id=_user['uid'])
	resultList = []
	for address in addressList:
		address = model_to_dict(address)
		address["addrid"]=address["adid"]
		del(address["user"])
		del(address["adid"])
		resultList.append(address)
	return Jsonify({"status":True, "error":"", "error_message":"", "addresslist":resultList})

@UserAuthorization
def changeNickname(request):
	_user = request.user
	nickname = request.POST.get("nickname", None)
	if not nickname:
		return Jsonify({"status":False, "error":"1101", "error_message":"信息不足, 请重新输入。"})
	userList = User.objects.filter(nickname = nickname)
	if userList:
		return Jsonify({"status":False, "error":"1108", "error_message":"昵称已被注册, 请重新输入。"})
	user = User.objects.filter(uid=_user['uid'])
	if user:
		user = user[0]
		user.nickname = nickname
		user.save()
		return Jsonify({"status":True, "error":"", "error_message":"", "addresslist":model_to_dict(user)})
	else:
		return Jsonify({"status":False, "error":"1113", "error_message":"用户不存在。"})

@UserAuthorization
def changePassword(request):
	_user = request.user
	password = request.POST.get("password", None)
	if not password:
		return Jsonify({"status":False, "error":"1101", "error_message":"信息不足, 请重新输入。"})
	if password == _user.password:
		return Jsonify({"status":False, "error":"1112", "error_message":"密码未改变， 请重新输入。"})
	#重新生成password和salt存入数据库， 并将新的session发给客户端。
	salt = Salt()
	timestamp = str(int(math.floor(time.time())))
	_hash = salt.hash(salt.md5(user['password']) + "|" + user['username'] + "|" + timestamp)
	password = salt.md5(_hash+salt.md5(user['password']))
	_user.password = password
	_user.salt = _hash
	_user.save()
	user = model_to_dict(_user)
	user["session"] = updateSession(user)
	return Jsonify({"status":True, "error":"", "error_message":"", "user":user})

@UserAuthorization
def updateAvatar(request):
	logger.debug("GET HERE!!!!!!!!!!!!!!!!!!!!!!!")
	avatar = request.FILES.get('avatar', None)
	_user = request.user
	user = User.objects.filter(uid=_user['uid'])
	if not user:
		return Jsonify({"status":False, "error":"1113", "error_message":"用户不存在。"})
	if not avatar:
		return Jsonify({"status":False, "error":"1101", "error_message":"信息不足, 请重新输入。"})
	user = user[0]
	currentPath = AVATARPATH+str(_user['uid'])+".png"
	data=""
	for chunk in avatar.chunks():
		data+=chunk
	try:
		state = Picture().uploadPicture(currentPath, data)
	except Exception, e:
		logger.debug("FAIL PICTURE SERVER")
		logger.debug(e)
		return Jsonify({"status":True, "error":"1111", "error_message":"上传图片超时。", "avatar":1})
	logger.debug("GET HERE4")
	if state:
		user.avatar=1
		user.save()
		return Jsonify({"status":True, "error":"", "error_message":"", "avatar":1})
	else:
		return Jsonify({"status":True, "error":"1109", "error_message":"图片上传失败, 替换为默认头像。", "avatar":1})
