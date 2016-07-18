from VIPSystem.models import VIP, VIPPackage
from datetime import datetime, timedelta

def changePackage(vip):
	#No need to flush
	vip.headPackage.days = 0
	vip.headPackage.save()
	if vip.headPackage.nextPackage:
		vip.headPackage.nextPackage.start_date = datetime.now()
		vip.headPackage.nextPackage.save()
	vip.headPackage = vip.headPackage.nextPackage
	vip.save()
	return vip

def flushVip(vip):
	if vip:
		total_timedelta = datetime.now() - vip.headPackage.start_date
		difference = total_timedelta - timedelta(vip.headPackage.days)
		while difference >= timedelta(0):
			total_timedelta = difference
			vip = changePackage(vip)	
			difference = total_timedelta - timedelta(vip.headPackage.days)
		vip.headPackage.days = vip.headPackage.days - total_timedelta.days
		vip.headPackage.save()
		return vip
	else:
		return vip

def addNewHeadPackage(vip, newPackage):
	vip = flushVip(vip)
	vip.headPackage.days = vip.headPackage.days - (datetime.now() - vip.headPackage.start_date)
	vip.headPackage.save()
	newPackage.nextPackage = vip.headPackage
	newPackage.start_date = datetime.now()
	newPackage.save()
	vip.headPackage = newPackage
	vip.save()
	return vip

def addNewPackage(month, typeid, vip=None):
	vip = flushVip(vip)
	if vip:
		currentPackage = vip.headPackage
		if currentPackage.level == typeid:
			currentPackage.days = currentPackage.days + month*31
			currentPackage.save()
		else:		
			if currentPackage.level < typeid:
				newPackage = VIPPackage(start_date = None, days = month*31, level=typeid, nextPackage=None)
				newPackage.save()
				vip = addNewHeadPackage(vip, newPackage)
			else:
				fatherPackage = None
				while currentPackage.level > typeid:
					fatherPackage = currentPackage
					currentPackage = currentPackage.nextPackage
				if currentPackage.level == typeid:
					currentPackage.days = currentPackage.days + month * 31
					currentPackage.save()
				else:
					newPackage = VIPPackage(start_date = None, days = month*31, level=typeid, nextPackage=currentPackage)
					newPackage.save()
					fatherPackage.nextPackage = newPackage
					fatherPackage.save()
		return vip				
	else:
		vip = VIP()
		vip.save()
		newPackage = VIPPackage(startdate = datetime.now(), days = month*31, level=typeid, vip_belong=vip)
		newPackage.save()
		vip.headPackage = newPackage
		vip.save()
		return vip


	
