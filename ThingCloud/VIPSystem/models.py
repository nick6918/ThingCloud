from django.db import models
from datetime import datetime, timedelta
from django.forms.models import model_to_dict
from TCD_lib.utils import dictPolish
from django.utils import timezone
import logging

logger = logging.getLogger('appserver')

# Create your models here.
class VIPPackage(models.Model):
	vpid = models.AutoField(primary_key = True)
	nextPackage = models.ForeignKey("self", null=True, default = None)
	start_date = models.DateTimeField(null=True, default = None)
	days = models.IntegerField()
	level = models.IntegerField()
	merged = models.IntegerField(default = 0)

	def merge(self, otherPackage):
		self.days = self.days + otherPackage.days
		self.save()
		otherPackage.merged = 1
		otherPackage.save()
		return self

	def insert(self, otherPackage):
		if self.nextPackage:
			otherPackage.nextPackage = self.nextPackage
			otherPackage.save()
		self.nextPackage = otherPackage
		self.save()
		return self

	class Meta:
		db_table = "package_vip"

class VIP(models.Model):
	"""
        VIP System for user.
    """

	vid = models.AutoField(primary_key = True)
	headPackage = models.ForeignKey(VIPPackage, null=True, default = None)

	def rotatePackage(self):
		if self.headPackage:
			self.headPackage.days = 0
			self.headPackage.save()
			if self.headPackage.nextPackage:
				self.headPackage.nextPackage.start_date = timezone.now()
				self.headPackage.nextPackage.save()
			self.headPackage = self.headPackage.nextPackage
			self.save()
		return self

	def flush(self):
		if self.headPackage:
			total_timedelta = timezone.now() - self.headPackage.start_date
			logger.debug(timezone.now())
			logger.debug(self.headPackage.start_date)
			logger.debug(total_timedelta.days)
			difference = total_timedelta - timedelta(self.headPackage.days)
			while difference >= timedelta(0):
				total_timedelta = difference
				self.rotatePackage()	
				difference = total_timedelta - timedelta(self.headPackage.days)
			self.headPackage.days = self.headPackage.days - total_timedelta.days
			self.headPackage.save()
		return self

	def addHeadPackage(self, newPackage):
		self.flush()
		if self.headPackage:
			self.headPackage.days = self.headPackage.days - (timezone.now() - self.headPackage.start_date).days
			self.headPackage.save()
			newPackage.nextPackage = self.headPackage
		newPackage.start_date = timezone.now()
		newPackage.save()
		self.headPackage = newPackage
		self.save()
		return self

	def addNewPackage(self, newPackage):
		self.flush()
		if self.headPackage:
			if self.headPackage.level < newPackage.level:
				self.addHeadPackage(newPackage)
			elif self.headPackage.level == newPackage.level:
				self.headPackage.merge(newPackage)
			else:
				#self.headPackage.level > newPackage.level
				currentPackage = self.headPackage
				while currentPackage.nextPackage:
					if currentPackage.nextPackage.level == newPackage.level:
						currentPackage.nextPackage.merge(newPackage)
					elif currentPackage.nextPackage.level > newPackage.level:
						currentPackage = currentPackage.nextPackage
					else:
						#currentPackage.nextPackage.level < newPackage.level
						currentPackage.insert(newPackage)
		else:
			self.addHeadPackage(newPackage)
		return self

	def getPackageList(self):
		currentPackage = self.headPackage
		resultList = []
		while currentPackage:
			current_dict = dictPolish(model_to_dict(currentPackage))
			resultList.append(current_dict)
			currentPackage = currentPackage.nextPackage
		return resultList

	def toDict(self):
		result = model_to_dict(self.headPackage)
		result["vid"] = self.vid
		result["end_date"] = result["start_date"] + timedelta(result["days"])
		return dictPolish(result)

	class Meta:

		db_table = "user_vip"
