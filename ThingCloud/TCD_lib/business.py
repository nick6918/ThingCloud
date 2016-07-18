from VIPSystem.models import VIP, VIPPackage
from datetime import datetime, timedelta

def changePackage(vip, nextPackage=None):
	vip.currentPackage.days = 0
	vip.currentPackage.save()
	if nextPackage:
		nextPackage.start_date = datetime.now()
		nextPackage.save()
	vip.currentPackage = nextPackage
	vip.save()
	return vip

def flushVip(vip):
	if vip:
		total_timedelta = datetime.now() - vip.currentPackage.start_date
		difference = total_timedelta - timedelta(vip.currentPackage.days)
		while difference >= timedelta(0):
			total_timedelta = difference
			nextPackage = VIPPackage.objects.filter(vid=vid).order_by("-level")
			if not nextPackage:
				changePackage(vip)
				return vip
			nextPackage = nextPackage[0] 
			vip = changePackage(vip, nextPackage)	
			difference = total_timedelta - timedelta(vip.currentPackage.days)
		vip.currentPackage.days = vip.currentPackage.days - total_timedelta.days
		vip.currentPackage.save()
		return vip
	else:
		return vip

def addVip(month, typeid, vip=None):
	vip = flushVip(vip)
	if vip:
		currentPackage = vip.currentPackage
		if currentPackage.level == typeid:
			currentPackage.days = currentPackage.days + month*31
			currentPackage.save()
		else:		
			newPackage = VIPPackage(start_date = None, days = month*31, level=typeid, vip_belong=vip)
			newPackage.save()
			if currentPackage.level < typeid:
				vip = changePackage(vip, newPackage)
			else:
				sameLevelPackage = VIPPackage.objects.filter(vip_belong=vip).filter(level=typeid)
				if sameLevelPackage:
					sameLevelPackage = sameLevelPackage[0]
					sameLevelPackage.days = sameLevelPackage.days + month * 31
					sameLevelPackage.save()
				else:
					newPackage = VIPPackage(startdate = datetime.now(), days = month*31, level=typeid, vip_belong=vip)
					newPackage.save()
	else:
		vip = VIP()
		vip.save()
		newPackage = VIPPackage(startdate = datetime.now(), days = month*31, level=typeid, vip_belong=vip)
		newPackage.save()
		vip.currentPackage = newPackage
		vip.save()
		return vip


	
