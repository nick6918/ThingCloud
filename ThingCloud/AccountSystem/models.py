from django.db import models

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
	avatar = models.BooleanField(default = False)
	username = models.CharField(max_length = 100, default = "WEIRDUSER")

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
