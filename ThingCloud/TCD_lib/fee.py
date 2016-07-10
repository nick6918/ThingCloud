# -*- coding: utf-8 -*-

def getVIPfee(month, level, typeid):
	#typeid:
	#1, 200Units
	#2, 500Units
	#3, Unlimited Units
	#month:

	fee = 0.1
	return fee

def getDeliveryfee(cmid):
	detail = u"同仓物流费用 6元"
	return (0.1, detail)

def feeList():
	origin = [50, 100, 150]
	current = [30, 50, 100]
	discount = [
	    {
	        "data":1,
	        "display":"一个月"
	    },
	    {
	        "data":1,
	        "display":"两个月"
	    },
	    {
	        "data":0.85,
	        "display":"三个月(八五折)"
	    },
	    {
	        "data":0.8,
	        "display":"六个月(八折)"
	    },
	    {
	        "data":0.7,
	        "display":"一年(七折)"
	    },
	    {
	        "data":0.6,
	        "display":"两年(六折)"
	    }]
	return origin, current, discount

