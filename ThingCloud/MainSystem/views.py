from django.shortcuts import render
from TCD_lib.utils import Jsonify
import logging

logger = logging.getLogger('appserver')

# Create your views here.
def index(request):
	logger.error("1213")
	return Jsonify("SUCCEED!")
