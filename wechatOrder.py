from Crypto.Hash import MD5
import random
import urllib2

APPID = 'wxc07a46ae58282528'
MCHID = '1361409502'

def generateRandomString(size):

    ALPHABET = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    result = ""
    for k in range(0, size):
        index = random.randint(0, 61)
        result += ALPHABET[index]
    return result

def unifyOrder(order, body, userip, detail):
	info = {}
	info['mch_id'] = MCHID
	info['app_id']  = APPID
	info['device_info']  = "WEB"
	info['nonce_str']  = generateRandomString(32)
	info['body']  = body
	info['detail']  = detail
	info['out_trade_no']  = order["oid"]
	info['fee_type']  = "CNY"
	info['fee']  = order["fee"]*100
	info['spbill_create_ip']  = userip
	info['notify_url']  = "testapi.thingcloud.net:8001/order/callback"
	info['trade_type']  = "APP"

	keylist = info.keys()
	keylist.sort()
	result = ""
	for item in keylist:
		if info[item]:
			current = item+"=" +str(info[item]) + "&"
			result += current
	result = result + "key=dfa3c2228afde6d006782cd901cc843c"
	sign=MD5(result).toUpperCase()
	xml = '<xml>/n'
	for key in keylist:
		xml = xml + "   <" + key + ">" + str(info[key]) + "</" + key +">/n"
	xml += '</xml>'
	request = urllib2.Request(url = url, headers = {'content-type':'text/xml'}, data = xml)
	response = urllib2.urlopen(request)
	content = response.read()
	return content

if __name__ == '__main__':
	print unifyOrder({"oid":10101111, "fee":1}, "test", "127.0.0.1", "test")