from django.shortcuts import render
from django.forms.models import model_to_dict 
from datetime import datetime
from TCD_lib.utils import get_client_ip, Jsonify
from TCD_lib.security import Salt
from models import User, UserRelation, UserSession
import time,math, logging
import logging
logger = logging.getLogger('appserver')

# Create your views here.

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
	user['nickname'] = request.POST.get("nickname", None)
	userList = User.objects.filter(nickname = user['nickname'])
	if userList:
		return Jsonify({"status":False, "error_code":"1106", "error_message":"nickname Already Taken"})
	user['loginIp'] = get_client_ip(request)
	user['registerTime'] = datetime.now()
	user['birthday'] = request.POST.get("birthday", "")
	user['password'] = request.POST.get("password", None)
	user['phone'] = request.POST.get("phone", None)
	gender = request.POST.get("gender", 2)
	user['gender'] = int(gender)
	if not (user['nickname'] and user['password'] and user['phone']):
		return Jsonify({"status":False, "error_code":"1107", "error_message":"Not enough infomation"})
	# avatar = request.File.get("avatar", None)
	avatar = None
	if avatar:
		user['hasAvatar'] = True
		#PictureModel.uploadPicture(avatar)
	else:
		user['hasAvatar'] = False
	salt = Salt()
	user['username'] = "USER"+salt.generateSalt(10) +"@thingcloud.com"
	timestamp = str(int(math.floor(time.time())))
	_hash = salt.hash(salt.md5(user['password']) + "|" + user['username'] + "|" + timestamp)
	password = salt.md5(_hash+salt.md5(user['password']))
	currentUser = User(gid = user["gid"], phone=user['phone'],nickname = user['nickname'], gender = user['gender'], birthday = user['birthday'], register = user['registerTime'], lastLogin = user['registerTime'], loginIp = user['ip'], avatar = ['hasAvatar'], salt = _hash, password = password, username = user['username'] )
	currentUser.save()
	user['uid'] = currentUser.uid
	user['session'] = createSession(user)
	return Jsonify({"status":True, "error_code":"", "error_message":"", "user":user})

def verifyCode(request):
	logger.debug("get here")
	phone = request.GET.get("phone", None)
	code = request.GET.get("code", None)
	logger.debug((phone, code))
	if not (phone and code):
		return Jsonify({"status":False, "error_code":"1107", "error_message":"Not enough message"})
	user = User.objects.filter(phone=phone)
	if user:
		user =  model_to_dict(user[0])
		return Jsonify({"status":False, "error_code":"1103", "error_message":"Phone number already registered"})
	else:
		#iMessage.send(phone, code)
		return Jsonify({"status":True})
	
def loginByPhone(request):
	"""
	login by phone, return dynamic session.
	"""
	phone = request.GET.get('phone', None)
	user_password = request.GET.get('password', None)
	if not (phone and user_password):
		return Jsonify({"status":False, "error_code":"1107", "error_message":"Not enough message"})
	user = User.objects.filter(phone = phone)
	salt = Salt()
	if not user:
		return Jsonify({"status":False, "error_code":"1105", "error_message":"Phone number is not registered"})
	user = model_to_dict(user[0])
	if user['password'] == salt.md5(user['salt']+salt.md5(user_password)):
		logger.debug(("#USER#", user))
		user['session'] = updateSession(user)
		#some info is not allowed to be known by clients
		del user['salt']
		del user['password']
		return Jsonify({"status":True, "error_code":"", "error_message":"", "user":user})
	else:
		return Jsonify({"status":False, "error_code":"1104", "error_message":"Password error, login failed"})
