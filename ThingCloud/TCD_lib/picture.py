from TCD_lib import settings
from TCD_lib.upyun.upyun import UpYun
STATIC_IMAGE_PATH = ""
# from multiprocessing import Process
import logging
logger= logging.getLogger('appserver')

UPYUNURL = "thingcloud-master.b0.upaiyun.com"

class Picture(object):
	def __init__(self, _conn=None):
		super(Picture, self).__init__()
		self.cursor = _conn
	def uploadPicture(self,path, data, callback=None):
		upyun = UpYun(settings.image_bucket, settings.image_user, settings.image_password,timeout=4)
		result=upyun.put(path, data, True)
		return result
