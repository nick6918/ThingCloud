def getVIPfee(month, level):
    discount = 1
    base = 30
    if month >= 12:
        discount = 0.8
    fee = int(base * month * discount)
    return fee

def getDeliveryfee():
	#TODO
	return 01