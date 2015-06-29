from django.shortcuts import render
from TCD_lib.utils import Jsonify
import logging

# Create your views here.
def index(request):
	return Jsonify("SUCCEED!")