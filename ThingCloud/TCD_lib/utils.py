from django.http import HttpResponse
from django.db import connection
from datetime import datetime
import random, hashlib, time
from Crypto.Hash import MD5
from TCD_lib.settings import APPID, MCHI
from django.core.serializers.json import DjangoJSONEncoder
import json
import urllib2

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

def iosOrder(prepayid):
    data = {
        "appid":APPID,
        "noncestr":generateRandomString(32),
        "package":"Sign=WXPay",
        "partnerid":MCHID,
        "prepayid":prepayid,
        "timestamp": int(time.time())
    }
    keylist = data.keys()
    keylist.sort()
    signString = ""
    for key in keylist:
        signString = signString + key + "=" + str(data[key])+"&"
    signString += "key=sharecloud885677sharecloud885677"
    sign = md5(signString).upper()
    data["sign"]=sign
    return data

def unifyOrder(order, body, detail, userip, ordertype):

    url = "https://api.mch.weixin.qq.com/pay/unifiedorder"

    info = {}
    info['mch_id'] = MCHID
    info['appid']  = APPID
    info['device_info']  = "WEB"
    info['nonce_str']  = generateRandomString(32)
    info['body']  = body
    info['detail']  = detail
    info['out_trade_no']  = order["oid"]
    info['fee_type']  = "CNY"
    info['total_fee']  = int(order["fee"]*100)
    info['spbill_create_ip']  = userip
    info["notify_url"]  = ""
    if ordertype = 0:
        #delivery order
        info['notify_url']  = "testapi.thingcloud.net:8001/order/callback"
    else:
        #vip order
        info['notify_url']  = "testapi.thingcloud.net:8001/vip/callback"
    info['trade_type']  = "APP"

    keylist = info.keys()
    keylist.sort()
    result = ""
    for item in keylist:
        if info[item]:
            current = item+"=" +str(info[item]) + "&"
            result += current
    result = result + "key=sharecloud885677sharecloud885677"
    #wechat sign example
    #result = "appid=wxd930ea5d5a258f4f&body=test&device_info=1000&mch_id=10000100&nonce_str=ibuaiVcKdpRxkhJA&key=192006250b4c09247ec02edce69f6a2d"
    #code: "9A0A8659F005D6984697E2CA0A9CF3B7"
    sign=md5(result).upper()
    
    #统一下单接口xml表单
    xml = '<xml>\n'
    for key in keylist:
        xml = xml + "   <" + key + ">" + str(info[key]) + "</" + key +">\n"
    xml = xml + "   <sign>"+str(sign)+"</sign>\n</xml>"
    
    fp=open("xml.txt", "w+")
    fp.write(xml)
    fp.close()

    request = urllib2.Request(url = url, headers = {'content-type':'text/xml'}, data = xml)
    response = urllib2.urlopen(request)
    content = response.read()
    return content