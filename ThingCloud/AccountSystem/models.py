from django.db import models

# Create your models here.

class User(models.Model):
	
	uid = models.AutoField(primary_key = True)
	gid = models.IntegerField(max_length = 10)
	nickname = models.CharField(max_length=200)
	gender = models.CharField(max_length = 10, choices = (('1', 'MALE'), ('2', 'FEMAIL')))
	birthday = models.CharField(max_length = 50)
	register = models.DateTimeField()
	lastLogin = models.DateTimeField()
	loginIp = models.CharField(max_length = 20)
	password = models.CharField(max_length = 200)
	salt = models.CharField(max_length = 200)
	phone = models.CharField(max_length = 100)
	
	class Meta:
		db_table = 'user'
	
class UserRelation(models.Model):
	urid = models.AutoField(primary_key = True)
	uid = models.IntegerField(max_length = 10)
	uuid = models.IntegerField(max_length = 10)
	
	class Meta:
		db_table = 'user_relation'
	