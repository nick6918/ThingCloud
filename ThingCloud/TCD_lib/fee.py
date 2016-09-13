# -*- coding: utf-8 -*-

def feeList():
	units = [100, 200, 500, 800, 1000, "unlimited"]
	#tt = [30, 60, 150, 240, 300]
	#% = [100, 83, 80, 71, 65]
	origin = [30, 50, 120, 170, 200, 300]
	current = [20/100.0, 30, 72, 95, 102, 120, 150]
	#current = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
	discount = [
	    {
	        "data":1,
	        "month":1,
	        "display":"一个月"
	    },
	    {
	        "data":1,
	        "month":2,
	        "display":"两个月"
	    },
	    {
	        "data":0.85,
	        "month":3,
	        "display":"三个月(八五折)"
	    },
	    {
	        "data":0.8,
	        "month":6,
	        "display":"六个月(八折)"
	    },
	    {
	        "data":0.7,
	        "month":12,
	        "display":"一年(七折)"
	    },
	    {
	        "data":0.6,
	        "month":24,
	        "display":"两年(六折)"
	    }]
	return origin, current, discount


def getVIPfee(month, level, typeid):
	#typeid:
	#1, 200Units
	#2, 500Units
	#3, Unlimited Units
	#month:
    origin, current, discount = feeList()
    disc = {}
    for item in discount:
    	disc[int(item['month'])] =item['data']
    fee = current[typeid] * month * disc[month]
    return fee

def getDeliveryfee(_user, cmid):
	if _user.vipinfo:
		detail = u'同仓物流费用 6元\n会员免费 0元'
		return (0, detail)
	else:
		detail = u"同仓物流费用 6元"
		return (0.1, detail)	

