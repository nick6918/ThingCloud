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
	discount = {
	    "1":(1, "原价"),
	    "2":(1, "原价"),
	    "3":(0.85, "15% OFF!"),
	    "6":(0.8, "20% OFF!"),
	    "12":(0.7, "30% OFF!"),
	    "24":(0.6, "40% OFF!")
	}
	return origin, current, discount

