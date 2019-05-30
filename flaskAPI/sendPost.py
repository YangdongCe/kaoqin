# -*- coding: utf-8 -*-
# @Time    : 2018/6/1 21:34
# @File    : sendPost.py
# @Software: PyCharm
import base64
import requests
import json
import numpy as np


def getFaceFeature(imgB64):
    """

    :param imgB64: 图片的base64编码
    :return: 128维特征向量 bytes
    """
    url='http://127.0.0.1:1080/api'
    data={'img':imgB64}
    response=requests.post(url,data=data)
    res=json.loads(response.text)
    face=np.array(res['faceFeature'])
    return face.tostring()

def getJWXTInfo(username,pwd):
    url = 'http://127.0.0.1:1080/jwxt'
    data = {'username': username,'pwd':pwd}
    response = requests.post(url, data=data)
    res = json.loads(response.text)
    return res
