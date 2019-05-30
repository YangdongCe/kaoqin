import io
from urllib import request
from urllib import error
from urllib import parse
import numpy as np
from http import cookiejar
import requests
from PIL import Image
from bs4 import BeautifulSoup

cookie = cookiejar.CookieJar()
cookie_support = request.HTTPCookieProcessor(cookie)
opener = request.build_opener(cookie_support)
user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.168 Safari/537.36"
head_c = {'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
          'User-Agent': user_agent, 'Connection': 'keep-alive',
          'Referer': 'http://jwxt.imu.edu.cn/login?errorCode=badCaptcha',
          'Accept-Encoding': 'gzip, deflate',
          'Host': 'jwxt.imu.edu.cn'
          }

def getCode():
    req_c = request.Request(url=' http://jwxt.imu.edu.cn/img/captcha.jpg', headers=head_c)
    try:
        response_c = opener.open(req_c)
        img_data = response_c.read()
        return img_data
    except error.URLError as e:
        if hasattr(e, 'code'):
            print("HTTPError:%d" % e.code)
        elif hasattr(e, 'reason'):
            print("URLError:%s" % e.reason)
        return b''

def Login(code,xuehao,mima):
    login_url = "http://jwxt.imu.edu.cn/j_spring_security_check"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.168 Safari/537.36"
    head = {'User-Agent': user_agent, 'Connection': 'keep-alive'}
    login_data = {}
    login_data['j_username'] = xuehao
    login_data['j_password'] = mima
    login_data['j_captcha'] = code
    loginpostdata = parse.urlencode(login_data).encode('utf-8')
    req = request.Request(url=login_url, data=loginpostdata, headers=head)
    try:
        response = opener.open(req)

        print(response.code)
        return True
    except error.URLError as e:
        if hasattr(e, 'code'):
            if e.code == 500:
                return False
        elif hasattr(e, 'reason'):
            return False
        return False

def getCodeRecognize(xuehao, mima):
    url = 'http://127.0.0.1:8888'
    i = 3
    while i != 0:
        i -= 1
        data = getCode()
        req = requests.post(url, files={'file': data})
        text = req.content.decode('ascii')
        if Login(text, xuehao, mima):
            print("success")
            # data = io.BytesIO(data)
            # img = Image.open(data)
            # print(text)
            break
        else:
            print(i, "fail")
    return opener

if __name__ == '__main__':
    getCodeRecognize('0161122147','wl19980805')
    data_url1 = "http://jwxt.imu.edu.cn/student/rollManagement/electronicRegistration/index"
    head = {'User-Agent': user_agent, 'Connection': 'keep-alive'}
    req1 = request.Request(url=data_url1, headers=head)
    response1 = opener.open(req1)
    html = response1.read().decode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    name = soup.find_all('div', class_="profile-info-value")[2].contents[0].replace(' ', '').strip('\n').replace(
        '\r',
        '').replace(
        '\n', '')
    print(name)
