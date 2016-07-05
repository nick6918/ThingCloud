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
    detail = models.CharField(max_length=300)
    code = models.CharField(max_length=50)
    showcode = models.CharField(max_length=50)
    message = models.CharField(max_length=300)
    state = models.IntegerField()

    class Meta:
    dsid = models.AutoField(primary_key=True)
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

class Version(models.Model):
    vrid = models.AutoField(primary_key=True)
    version = models.CharField(max_length=50)
    state = models.IntegerField()
    typeid = models.IntegerField()
    compulsorylist = models.CharField(max_length=300)
    selectlist = models.CharField(max_length=300)
    compulsorynotes = models.CharField(max_length=300)
    notes = models.CharField(max_length=300)
    devnotes = models.CharField(max_length=300)

    class Meta:
		db_table = 'meta_version'

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
    district_belong = models.ForeignKey(District)

    class Meta:
        db_table = 'meta_commuties'




