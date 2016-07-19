from VIPSystem.models import VIP, VIPPackage
from AccountSystem.models import User
from datetime import datetime, timedelta
from django.utils import timezone

def changePackage(vip):
	#No need to flush
	vip.headPackage.days = 0
	vip.headPackage.save()
	if vip.headPackage.nextPackage:
		vip.headPackage.nextPackage.start_date = timezone.now()
		vip.headPackage.nextPackage.save()
	vip.headPackage = vip.headPackage.nextPackage
	vip.save()
	return vip

def flushVip(vip):
	if vip:
		total_timedelta = timezone.now() - vip.headPackage.start_date
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
	vip.headPackage.days = vip.headPackage.days - (timezone.now() - vip.headPackage.start_date).days
	vip.headPackage.save()
	newPackage.nextPackage = vip.headPackage
	newPackage.start_date = timezone.now()
	newPackage.save()
	vip.headPackage = newPackage
	vip.save()
	return vip

def addNewPackage(month, typeid, vip=None, user=None):
	if type(user) == dict:
		user = User.objects.filter(uid=user['uid'])[0]
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
		newPackage = VIPPackage(start_date = timezone.now(), days = month*31, level=typeid)
		newPackage.save()
		vip.headPackage = newPackage
		vip.save()
		user.vip = vip
		user.save()
		return vip


	
