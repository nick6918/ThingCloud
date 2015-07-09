from django.db import models

# Create your models here.

class User(models.Model):
	"""
	Basic user info.
	"""
	uid = models.AutoField(primary_key = True)
	gid = models.IntegerField(max_length = 10)
	nickname = models.CharField(max_length=200)
	gender = models.IntergerField()
	birthday = models.CharField(max_length = 50)
	register = models.DateTimeField()
	lastLogin = models.DateTimeField()
	loginIp = models.CharField(max_length = 20)
	password = models.CharField(max_length = 200)
	salt = models.CharField(max_length = 200)
	phone = models.CharField(max_length = 100)
	avatar = models.BooleanField(default = False)
	username = models.CharField(max_length = 100, default = "WEIRDUSER")
	
	class Meta:
		db_table = 'user'
	
class UserRelation(models.Model):
	"""
	The model is to record the relationship between temporary account and user account;
	Once an temp account is logged in by an user, it is record here.
	"""
	urid = models.AutoField(primary_key = True)
	uid = models.IntegerField(max_length = 10)
	uuid = models.IntegerField(max_length = 10)
	
	class Meta:
		db_table = 'user_relation'
		
class UserSession(models.Model):
	"""
	This is the session table to give user dynamic authorization info.
	"""
	uid = models.IntegerField(primary_key = True)
	session_password = models.CharField(max_length = 100)
	
	class Meta:
		db_table = 'user_session'
	
