from django.db import models

# Create your models here.
class VIPPackage(models.Model):
	vpid = models.AutoField(primary_key = True)
	nextPackage = models.ForeignKey("self", null=True, default = None)
	start_date = models.DateTimeField()
	days = models.IntegerField()
	level = models.IntegerField()

	class Meta:
		db_table = "package_vip"

class VIP(models.Model):
    """
        VIP System for user.
    """

    vid = models.AutoField(primary_key = True)
    headPackage = models.ForeignKey(VIPPackage, null=True, default = None)

    class Meta:

        db_table = "user_vip"
