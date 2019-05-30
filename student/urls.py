from django.conf.urls import url, include
from django.contrib import admin
from student import views


app_name = "student"

urlpatterns = [
    url(r'^$', views.sLogin, name="sIndex"),
    url(r'^sLogin$', views.sLogin, name="sLogin"),
    url(r'^sRegister$', views.sRegister, name="sRegister"),
    url(r'^sRegisterInfo$', views.sRegisterInfo, name="sRegisterInfo"),
    url(r'^sLoginInfo$',views.sLoginInfo, name="sLoginInfo"),
    url(r'^sSignPage$', views.sSignPage, name="sSignPage"),
    url(r'^sSingInfo$', views.sSingInfo, name="sSingInfo"),


    url(r'^srImage$', views.srImage, name="srImage"),
    url(r'^sLoginImage$', views.sLoginImage, name="sLoginImage"),
    url(r'^sPage$', views.sPage, name="sPage"),
    url(r'^sSetSign$', views.sSetSign, name="sSetSign"),
]
