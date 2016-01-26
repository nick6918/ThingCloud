# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.forms.models import model_to_dict
from datetime import datetime
from TCD_lib.utils import get_client_ip, Jsonify
from TCD_lib.security import Salt
from TCD_lib.picture import Picture, UPYUNURL
from models import User, UserSession, Code
import time,math, logging, random
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
	_code = request.POST.get('code', None)
	if not (user['nickname'] and user['password'] and user['phone'] and _code):
		return Jsonify({"status":False, "error":"1101", "error_message":"Not enough infomation"})
	code = Code.objects.filter(phone=user['phone'])
	if not code or (_code != unicode(code[0].code)):
		return Jsonify({"status":False, "error":"1104", "error_message":"Security code error"})
	userList = User.objects.filter(nickname = user['nickname'])
	if userList:
		return Jsonify({"status":False, "error":"1108", "error_message":"nickname Already Taken"})
	userList = User.objects.filter(phone=user['phone'])
	if userList:
		return Jsonify({"status":False, "error":"1105", "error_message":"phone number Already Taken"})
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
			return Jsonify({"status":False, "error":"1109", "error_message":"Picture upload error, replaced by default.", "user":user})
		except Exception, e:
			logger.error("upload error")
			logger.error(e)
			return Jsonify({"status":False, "error":"1109", "error_message":"Picture upload error, replaced by default."})
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
		return Jsonify({"status":False, "error":1101, "error_message":"Not enough message"})
	phone=int(phone)
	print phone
	user = User.objects.filter(phone=phone)
	if user:
		return Jsonify({"status":False, "error":1105, "error_message":"Phone number already registered"})
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

def loginByPhone(request):
	"""
	login by phone, return dynamic session.
	"""
	phone = request.GET.get('phone', None)
	user_password = request.GET.get('password', None)
	if not (phone and user_password):
		return Jsonify({"status":False, "error":"1101", "error_message":"Not enough message"})
	user = User.objects.filter(phone = phone)
	salt = Salt()
	if not user:
		return Jsonify({"status":False, "error":"1107", "error_message":"Phone number is not registered"})
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
		return Jsonify({"status":False, "error":"1106", "error_message":"Password error, login failed"})
