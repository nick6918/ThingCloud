from django.db import models
from AccountSystem.models import Address, User

# Create your models here.
class Order(models.Model):

    oid = models.AutoField(primary_key=True)
    addr = models.ForeignKey(Address)
    user = models.ForeignKey(User)
    notes = models.CharField(max_length=300)
    fee = models.IntegerField()
    typeid = models.IntegerField()
    itemList = models.CharField(max_length=200)
    state = models.IntegerField()
    create_time = models.DateTimeField()
    paid_time = models.DateTimeField()
    finish_time = models.DateTimeField()
    prepayid = models.CharField(max_length=50)

    class Meta:

        db_table = "orders"

class Complaint(models.Model):
    cmpid = models.AutoField(primary_key=True)
    state = models.IntegerField()
    notes = models.CharField(max_length=300)
    user = models.ForeignKey(User)
    order = models.ForeignKey(Order)

    class Meta:
        db_table = "Complaints"
