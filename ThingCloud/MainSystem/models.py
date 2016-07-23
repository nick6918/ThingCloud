from django.db import models
from AccountSystem.models import User

# Create your models here.
class Employee(models.Model):
	"""docstring for Employee"""
	eid = models.AutoField(primary_key=True)
	user = models.OneToOneField(User, null=True)
	phone = models.CharField(max_length=50)
	name = models.CharField(max_length=50)

	class Meta:
		db_table = "work_employee"

