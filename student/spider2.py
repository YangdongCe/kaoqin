
#爬  姓名， 班级， 性别， 专业， 系， 班级
from urllib import request
from urllib import error
from urllib import parse
from http import cookiejar
from bs4 import BeautifulSoup
from codeRecognize import getCodeRecognize

def getMessage2(xuehao='0161122147', mima='wl19980805'):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.168 Safari/537.36"
    head = {'User-Agent': user_agent, 'Connection': 'keep-alive'}
    opener = getCodeRecognize(xuehao, mima)
    data_url1 = "http://jwxt.imu.edu.cn/student/rollManagement/electronicRegistration/index"
    req1 = request.Request(url=data_url1, headers=head)
    try:

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

