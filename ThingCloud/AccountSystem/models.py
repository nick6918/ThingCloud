# -*- coding: utf-8 -*-

from django.db import models
from django.forms.models import model_to_dict
from VIPSystem.models import VIP

# Create your models here.

class User(models.Model):
	"""
	Basic user info.
	"""
	uid = models.AutoField(primary_key = True)
	gid = models.IntegerField()
	nickname = models.CharField(max_length=200)
	gender = models.IntegerField()
	birthday = models.CharField(max_length = 50)
	register = models.DateTimeField()
	lastLogin = models.DateTimeField()
	loginIp = models.CharField(max_length = 20)
	password = models.CharField(max_length = 200)
	salt = models.CharField(max_length = 200)
	phone = models.CharField(max_length = 100)
	avatar = models.IntegerField()
	username = models.CharField(max_length = 100, default = "WEIRDUSER")
	vip = models.ForeignKey(VIP, null=True)

	class Meta:
		db_table = 'user'

	def toDict(self):
		_user = model_to_dict(self)
		if self.vip:
			self.vip.flush()
			_vip = self.vip.toDict()
			_user["vipinfo"] = _vip
		else:
			_user["vipinfo"] = ""
		del(_user['loginIp'])
		del(_user['lastLogin'])
		del(_user['salt'])
		del(_user['password'])
		del(_user['register'])
		return _user


class UserSession(models.Model):
	"""
	This is the session table to give user dynamic authorization info.
	"""
	uid = models.IntegerField(primary_key = True)
	session_password = models.CharField(max_length = 100)

	class Meta:
		db_table = 'user_session'

class Code(models.Model):
	phone = models.CharField(primary_key=True, max_length=50)
	code = models.IntegerField()

	class Meta:
		db_table = 'code_by_phone'

class InviteCode(models.Model):
	icid = models.AutoField(primary_key=True)
	state = models.IntegerField()
	code = models.CharField(max_length=50)
	notes = models.CharField(max_length=100)

	class Meta:
		db_table = 'meta_invite'
