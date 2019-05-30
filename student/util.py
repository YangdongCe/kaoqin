
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

def computeDistince(feature1,feature2):
    """

    :param feature1: 二进制特征向量
    :param feature2: 二进制特征向量
    :return: 两个特征向量的欧氏距离
    """
    f1 = np.fromstring(feature1, dtype=float)
    f2 = np.fromstring(feature2, dtype=float)
    dist = np.sqrt(np.sum(np.square(f1 - f2)))
    return dist
if __name__=='__main__':
    imgDir='./test.jpg'
    img=open(imgDir,'rb')
    imgB64=base64.b64encode(img.read())
    faceFeature=getFaceFeature(imgB64)
    print(faceFeature)