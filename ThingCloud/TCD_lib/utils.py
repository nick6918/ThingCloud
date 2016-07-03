from django.http import HttpResponse
from django.db import connection
from datetime import datetime
import random
import hashlib
from Crypto.Hash import MD5
from django.core.serializers.json import DjangoJSONEncoder
import json

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class Jsonify(HttpResponse):
	"""docstring for jsonify"""
	def __init__(self,content='',*arg, **kw):
		super(Jsonify, self).__init__(content,*arg, **kw)
		self.content = json.dumps(content,indent=4,sort_keys=True,cls=DjangoJSONEncoder,ensure_ascii=False)
		self['Content-Type']='application/json; charset=utf-8'
		self['Vary']= 'Accept-Encoding'
		self['Content-Length'] = len(self.content)

def dictPolish(jDict):
    result = {}
    for item in jDict.keys():
        if type(jDict[item])==datetime:
            result[item]=jDict[item].strftime('%Y/%m/%d %T')
        elif jDict[item]==None:
            result[item]=""
        else:
            result[item]=jDict[item]
    return result

def generateRandomString(size):

    ALPHABET = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    result = ""
    for k in range(0, size):
        index = random.randint(0, 61)
        result += ALPHABET[index]
    return result

def md5(src):
    m2 = hashlib.md5()
    m2.update(src)
    return m2.hexdigest()
