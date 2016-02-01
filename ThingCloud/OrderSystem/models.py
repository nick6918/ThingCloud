from django.db import models

# Create your models here.
class Order(models.Model):

    oid = models.IntegerField(primary_key=True)
    addr = ForeignKey(Address)
    phone = CharField(max_length=50)
    gender = IntegerField(max_length=50)
    name = CharField(max_length=100)
    notes = CharField(max_length=300)
    fee = IntegerField()
    typeid = IntegerField()
    itemList = CharField(max_length=200)
    state = IntegerField()
    pay_state = IntegerField()
    create_time = DateTimeField()
    paid_time = DateTimeField()
    finish_time = DateTimeField()

    class Meta:

        db_table = order
