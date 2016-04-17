from django.db import models
from AccountSystem.models import User

# Create your models here.

class Feedback(models.Model):
    fdid = models.AutoField(primary_key=True)
    notes = models.CharField(max_length=300)
    user = models.ForeignKey(User)
    state = models.IntegerField()

    class Meta:
        db_table="feedbacks"

class Discount(models.Model):
    dsid = models.AutoField(primary_key=True)
    detail = models.CharField(max_length=300)
    code = models.CharField(max_length=50)
    showcode = models.CharField(max_length=50)
    message = models.CharField(max_length=300)
    state = models.IntegerField()

    class Meta:
        db_table="discount"

class Activity(models.Model):
    acid = models.AutoField(primary_key=True)
    state = models.IntegerField()
    priority = models.IntegerField()
    name = models.CharField(max_length=200)
    discount = models.ForeignKey(Discount)
    remark = models.CharField(max_length=200)
    bannerurl = models.CharField(max_length=150)
    url = models.CharField(max_length=150)

    class Meta:
		db_table = 'activity'
