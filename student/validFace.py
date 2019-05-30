# -*- coding: utf-8 -*-
# @Time    : 2018/6/4 18:37
# @File    : AipFace.py
# @Software: PyCharm
import base64
""" 你的 APPID AK SK """
APP_ID = '11349285'
API_KEY = 'Y43n70UzibDF2l0QG3ulvxsc'
SECRET_KEY = 'wrMKcGZLZvZ4Tv002TtU0HuQOgiQNDE4'

import urllib, urllib.request, sys
from json import JSONDecoder

# 获取access_token
# host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Y43n70UzibDF2l0QG3ulvxsc&client_secret=wrMKcGZLZvZ4Tv002TtU0HuQOgiQNDE4'
# request = urllib.request.Request(host)
# request.add_header('Content-Type', 'application/json; charset=UTF-8')
# response = urllib.request.urlopen(request)
# content = response.read()
# print(content)
import re
from io import BytesIO

from PIL import Image
import os


def base64_to_image(base64_str):
    byte_data = base64.b64decode(base64_str)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)

    return img
def image_to_base64(image_path):
    img = Image.open(image_path)
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str

def detectiveFace(imgBase64):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        http_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
        data = {"access_token": "24.d29490bf4dafd261f7144c1b5f98c804.2592000.1561108982.282335-16318030",
                "Content-Type":"application/json",
                "image_type": "BASE64",
                "image": imgBase64
                }
        # 编码
        data = urllib.parse.urlencode(data).encode('utf-8')
        response = urllib.request.Request(url=http_url, data=data, headers=headers)
        req = urllib.request.urlopen(response, timeout=5)
        content = req.read().decode('utf-8')
        req_dict = JSONDecoder().decode(content)

        req.close()
        if req_dict["error_code"]==0 and req_dict["error_msg"]=='SUCCESS':
            if req_dict.get('result').get('face_num')==1:
                location = req_dict.get('result').get('face_list')[0].get('location')
                left=location['left']
                top = location['top']
                width = location['width']
                height= location['height']
                from matplotlib import pyplot as plt
                img=base64_to_image(imgBase64)
                imgCrop=img.crop((left,top,left+width,top+height))
                savePath=os.path.join('student/tempImg/test.jpg')
                imgCrop=imgCrop.convert('RGB')
                imgCrop.save(savePath)

                base64_str = image_to_base64(savePath)
                return {'state':1,'imgBase64':base64_str}

        return {'state':0}
    except urllib.error.HTTPError as err:
        raise ConnectionError

if __name__=='__main__':
    import time
    start = time.time()
    imgDir='./test.jpg'
    img = open(imgDir,'rb')
    imgB64 = base64.b64encode(img.read())
    res = detectiveFace(imgB64)
    print(res)
    print(time.time()-start)