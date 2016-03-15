from django.db import models

# Create your models here.
class VIP(models.Model):
    """
        VIP System for user.
    """

    vid = models.AutoField(primary_key = True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    level = models.IntegerField()

    class Meta:

        db_table = "user_vip"
