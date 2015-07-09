import math
from Crypto.Hash import MD5,SHA
import time,random
import logging
from django.db import connection
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
