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
    state = models.IntegerField()

    class Meta:
        db_table="discount"
