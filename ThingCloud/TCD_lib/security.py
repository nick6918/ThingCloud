# -*- coding: utf-8 -*-

import math
#Crypto.Hash belongs to library pycrypto
#but the lib that is install by pip seems problematic,
#instead, using easy_install pycrypto can solve this problem.
from Crypto.Hash import MD5,SHA
from django.forms.models import model_to_dict
import time,random
import logging
from django.db import connection
from AccountSystem.models import User, UserSession
from TCD_lib.utils import Jsonify

logger = logging.getLogger('appserver')

class Salt(object):
	def __init__(self):
		self.SaltLength=9
	def hash(self,password):
		return self.createHash(password)
	def createHash(self,password):
		_salt=self.generateSalt(self.SaltLength)
		_hash = self.md5(password + _salt)
		return _salt + _hash
	def validateHash(self,_hash,password):
		_salt =_hash[0:self.SaltLength]
		validHash = _salt + self.md5(password + _salt)
		return _hash == validHash
	def validate(self,_hash,password):
		return self,validateHash(_hash,password)
	def generateSalt(self,_len):
		_set = '0123456789abcdefghijklmnopqurstuvwxyzABCDEFGHIJKLMNOPQURSTUVWXYZ'
		setLen = len(_set)
		_salt = ''
		for i in range(_len):
			p = int(math.floor(random.random()* setLen))
			_salt += _set[p]
		return _salt
	def md5(self,string):
		p=MD5.new()
		p.update(string)
		return p.hexdigest()
	def checkSignature(self,query,token):
		signature = query.get('signature')
		timestamp = query.get('timestamp')
		nonce = query.get('nonce')
		now= math.ceil(time.time())
		if now - int(timestamp) > 43200:
			return False
		shasum = SHA.new()
		arr= [ token , timestamp , nonce]
		arr.sort()
		shasum.update(''.join(arr))
		logger.debug('signature: '+signature)
		logger.debug(shasum.hexdigest())
		return shasum.hexdigest() == signature

def UserAuthorization(func):
	"""
		Requre the function it decorated with request as its first Parameters.
	"""
	user = {}
	def inner(request,*av,**kw):
		print request.META
		user = {}
		if not 'HTTP_AUTHORIZATION' in request.META:
			return Jsonify({"error":"1102", "error_message":"用户未登录, 无session。", "status":False})
		else:
			auth = request.META['HTTP_AUTHORIZATION']
			auth = auth.strip().decode('base64')
			user['username'], user['password'] = auth.split(':')
			if user['username']=='' or user['password']=='':
				return Jsonify({"error":"1102", "error_message":"用户未登录。", "status":False})
			else:
				_session_info = UserSession.objects.filter(session_password=user['password'])
				if not _session_info:
					return Jsonify({"error":"1102", "error_message":"用户未登录, wrong session。", "status":False})
			 	else:
					_session_info = model_to_dict(_session_info[0])
					print _session_info
					_uid = _session_info['uid']
					_user = User.objects.filter(uid=_uid)
					if not _user:
						return Jsonify({"error":"1103", "error_message":"用户不存在。", "status":False})
					else:
						_user = _user[0]
					 	request.user=user.toDict()
		return func(request, *av, **kw)
	return inner
