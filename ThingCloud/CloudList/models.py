# -*- coding: utf-8 -*-

from django.db import models
from AccountSystem.models import User
from django.forms.models import model_to_dict

from TCD_lib.settings import UPYUNURL, AVATARPATH, PICURL
# Create your models here.

class WareHouse(models.Model):
	wid = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 50)
	addr = models.CharField(max_length = 200)
	typeid = models.IntegerField()

	class Meta:
		db_table = "warehouses"

class City(models.Model):
    ctid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'city'

class District(models.Model):
    dsid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    city_belong = models.ForeignKey(City)

    class Meta:
        db_table = 'districts'

class Community(models.Model):
    cmid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    state = models.IntegerField()
    district_belong = models.ForeignKey(District)
    wh_in = models.ForeignKey(WareHouse)

    class Meta:
        db_table = 'communities'

class Address(models.Model):
	adid = models.AutoField(primary_key=True)
	user = models.ForeignKey(User)
	addr = models.CharField(max_length=200)
	phone = models.CharField(max_length=50)
	name = models.CharField(max_length=100)
	gender = models.IntegerField()
	community_belong = models.ForeignKey(Community)
	is_default = models.IntegerField()
	tagid = models.IntegerField()
	#1 表示正在使用， 0表示已被用户删除， 2表示 异常。
	state = models.IntegerField()

	class Meta:
		db_table = 'addresses'

	def toDict(self):
		_address = model_to_dict(self)
		_address["city"] = self.community_belong.district_belong.city_belong.name
		_address["district"] = self.community_belong.district_belong.name
		_address["community"] = self.community_belong.name
		_address["whid"] = self.community_belong.wh_in.wid
		_address["wh_name"] = self.community_belong.wh_in.name
		return _address

class Thing(models.Model):
	tid = models.AutoField(primary_key = True)
	user_belong_to = models.ForeignKey(User)
	wh_in = models.ForeignKey(WareHouse)
	name = models.CharField(max_length = 100)
	notes = models.CharField(max_length = 200)
	time_saved = models.DateTimeField()
	state = models.IntegerField()
	typeid = models.IntegerField()
	#0 for books, 1 for clothes, 2 for pants and dress, 3 for shoes
	#4 for tools, 5 for electronics, 6 for bags and boxes, 7 for others
	subtype_name = models.CharField(max_length = 100)
	units = models.IntegerField()
	#0 for female, 1 for male, 2 for suiting for both
	gender = models.IntegerField()
	avatar = models.IntegerField()
	present_id = models.IntegerField(null=True, default=None)
	
	class Meta:
		db_table = 'things'

	def toDict(self):
		result = model_to_dict(self)
		result["wh_id"]= self.wh_in.wid
		result["wh_name"] = self.wh_in.name
		del(result['user_belong_to'])
		del(result['time_saved'])
		del(result['state'])
		if result['present_id']:
			result['avatarurl'] = PICURL+"thing/present"+str(result['present_id'])+".png"
		else:
			if int(result['avatar'])==1:
				result['avatarurl'] = PICURL+"thing/"+str(result['tid'])+".png"
			else:
				result['avatarurl'] = PICURL+"thing/default.png"
		for item in result.keys():
			logger.debug((item, type(result[item])))
		return result
