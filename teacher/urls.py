from django.conf.urls import url, include
from django.contrib import admin
from teacher import views

app_name = "teacher"


urlpatterns = [
    url(r'^$', views.tIndex, name="tIndex"),
    url(r'^tLogin$', views.tLogin, name='tLogin'),
    url(r'^tRegister$', views.tRegister, name='tRegister'),
    url(r'^tLoginInfo$', views.tLoginInfo, name="tLoginInfo"),
    url(r'^tRegisterInfo$', views.tRegisterInfo, name="tRegisterInfo"),

    url(r'^tPage$', views.tPage, name="tPage"),
    url(r'^tSignpage$', views.tSignpage, name="tSignpage"),
    url(r'^tPub$', views.tPub, name="tPub"),
    url(r'^tSetSign$',views.tSetSign,name='tSetSign'),
    url(r'^updateSignInfo$',views.updateSignInfo,name='updateSignInfo')

]
