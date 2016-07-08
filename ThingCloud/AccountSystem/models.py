# -*- coding: utf-8 -*-

from django.db import models
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
	vip = models.ForeignKey(VIP)

	class Meta:
		db_table = 'user'


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
		db_table = 'user_address'

class City(models.Model):
    ctid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'meta_city'

class District(models.Model):
    dsid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    city_belong = models.ForeignKey(City)

    class Meta:
        db_table = 'meta_districts'

class Community(models.Model):
    cmid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    state = models.IntegerField()
    district_belong = models.ForeignKey(District)

    class Meta:
        db_table = 'meta_commuties'

