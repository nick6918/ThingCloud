"""ThingCloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from MainSystem.views import index
from AccountSystem.views import loginByPhone, register, sendCode, address, addressList, deleteAddress, changePassword, changeNickname, updateAvatar
from CloudList.views import addNewItem, getItemList, modifyNotes
from OrderSystem.views import generateOrder, modifyOrder, confirmOrder, getOrderList, cancel, complain, update, orderCallback, getOrder, delete, vipCallback
from AssistSystem.views import feedback, checkDiscount, activityList, versionInfo, communityList,getFeeList, joinUs
from VIPSystem.views import vip, vipOrder, vipConfirm

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r"^index$", index),
    url(r"^account/sendcode$", sendCode),
    url(r"^account/register$", register),
    url(r"^account/login$", loginByPhone),
    url(r"^account/avatar$", updateAvatar),
    url(r"^account/address$", address),
    url(r"^account/addressdelete$", deleteAddress),
    url(r"^account/addresslist$", addressList),
    url(r"^account/password$", changePassword),
    url(r"^account/nickname$", changeNickname),
    url(r"^cloudlist/additem$", addNewItem),
    url(r"^cloudlist/getlist$", getItemList),
    url(r"^cloudlist/modifynotes$", modifyNotes),
    url(r"^order/generate$", generateOrder),
    url(r"^order/address$", modifyOrder),
    url(r"^order/confirm$", confirmOrder),
    url(r"^order/order$", getOrder),
    url(r"^order/orderlist$", getOrderList),
    url(r"^order/cancel$", cancel),
    url(r"^order/complain$", complain),
    url(r"^order/delete$", delete),
    url(r"^order/update$", update),
    url(r"^order/callback$", orderCallback),
    url(r"^assist/feedback$", feedback),
    url(r"^assist/discount$", checkDiscount),
    url(r"^assist/activitylist", activityList),
    url(r"^assist/version", versionInfo),
    url(r"^assist/communitylist", communityList),
    url(r"^assist/feelist", getFeeList),
    url(r"^assist/joinus", joinUs),
    url(r"^vip/vip$", vip),
    url(r"^vip/order$", vipOrder),
    url(r"^vip/confirm$", vipConfirm),
    url(r"^vip/callback$", vipCallback),
]
