
#爬  姓名， 班级， 性别， 专业， 系， 班级
from urllib import request
from urllib import error
from urllib import parse
from http import cookiejar
from bs4 import BeautifulSoup
from PIL import Image


def getMessage2(xuehao='0161122147', mima='0161122147'):
    login_url = "http://jwxt.imu.edu.cn/j_spring_security_check"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.168 Safari/537.36"
    head = {'User-Agent': user_agent, 'Connection': 'keep-alive'}
    head_c = {'Accept':'image/webp,image/apng,image/*,*/*;q=0.8',
              'User-Agent': user_agent, 'Connection': 'keep-alive',
              'Referer': 'http://jwxt.imu.edu.cn/login?errorCode=badCaptcha',
              'Accept-Encoding': 'gzip, deflate',
              'Host': 'jwxt.imu.edu.cn'
              }

    # form data信息
    # j_username:0161122147
    # j_password:0161122147
    # j_captcha1:error
    login_data = {}
    login_data['j_username'] = xuehao
    login_data['j_password'] = mima
    login_data['j_captcha1'] = 'error'

    loginpostdata = parse.urlencode(login_data).encode('utf-8')

    cookie = cookiejar.CookieJar()
    cookie_support = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_support)
    # code = request.Request(url=' http://jwxt.imu.edu.cn/img/captcha.jpg',headers=head)
    # print(code)
    req = request.Request(url=login_url, data=loginpostdata, headers=head)
    req_c = request.Request(url=' http://jwxt.imu.edu.cn/img/captcha.jpg',headers=head_c)
    data_url1 = "http://jwxt.imu.edu.cn/student/rollManagement/electronicRegistration/index"
    # data_data1 = {}
    # data_data1['ff'] = 'f'
    # data_data1['planNumber'] = ''
    req1 = request.Request(url=data_url1, headers=head)
    try:
        response_c = opener.open(req_c)
        # print(response_c)
        img_data = response_c.read()

        file = "code.png"
        playFile = open(file, 'wb')
        playFile.write(img_data)
        playFile.close()

        exit(1)
        response = opener.open(req)

        #print(html)
        response1 = opener.open(req1)
        html = response1.read().decode('utf-8')
        #
        # print(type(html))
        # print(html)
        soup = BeautifulSoup(html, "html.parser")
        # print(soup.find_all('div',class_="profile-info-value"))
        # print(len(soup.find_all('div', class_="profile-info-value")))
        # # for tag in soup.find_all('div',class_="profile-info-value"):
        # #     print(tag.contents[0].replace(' ', '').strip('\n'))
        # #     print(len(tag.contents[0].replace(' ', '').strip('\n')))
        # #名字
        # print(soup.find_all('div', class_="profile-info-value")[2].contents[0].replace(' ', '').strip('\n'))
        # #男 性别
        # print(soup.find_all('div', class_="profile-info-value")[3].contents[0].replace(' ', '').strip('\n'))
        # #系 软件工程系
        # print(soup.find_all('div', class_="profile-info-value")[4].contents[0].replace(' ', '').strip('\n'))
        # #专业  软件工程
        # print(soup.find_all('div', class_="profile-info-value")[5].contents[0].replace(' ', '').strip('\n'))
        # #班级   软件工程16级1班
        # print(soup.find_all('div', class_="profile-info-value")[6].contents[0].replace(' ', '').strip('\n'))

        name = soup.find_all('div', class_="profile-info-value")[2].contents[0].replace(' ', '').strip('\n').replace('\r','').replace('\n','')
        gender = soup.find_all('div', class_="profile-info-value")[3].contents[0].replace(' ', '').strip('\n').replace('\r','').replace('\n','')
        xi = soup.find_all('div', class_="profile-info-value")[4].contents[0].replace(' ', '').strip('\n').replace('\r','').replace('\n','')
        zhuanye = soup.find_all('div', class_="profile-info-value")[5].contents[0].replace(' ', '').strip('\n').replace('\r','').replace('\n','')
        banji = soup.find_all('div', class_="profile-info-value")[6].contents[0].replace(' ', '').strip('\n').replace('\r','').replace('\n','')
        return name, gender, xi, zhuanye, banji

    except error.URLError as e:
        if hasattr(e, 'code'):
            print("HTTPError:%d" % e.code)
        elif hasattr(e, 'reason'):
            print("URLError:%s" % e.reason)


if __name__ == '__main__':
    print(getMessage2())

