# -*- coding: utf-8 -*-

from django.shortcuts import render
from models import Feedback
from TCD_lib.utils import Jsonify
from TCD_lib.security import UserAuthorization
from django.forms.models import model_to_dict

# Create your views here.
@UserAuthorization
def feedback(request):
    _user = request.user
    notes = request.POST.get("notes", None)
    if not notes:
        return Jsonify({"status":False, "error":1101, "error_message":"信息不足, 请重新输入。"})
    fdback = Feedback(notes=notes, user_id=_user['uid'], state=0)
    fdback.save()
    return Jsonify({"status":True, "feedback":model_to_dict(fdback), "error":"", "error_message":""})
