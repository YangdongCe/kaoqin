from urllib import request
from urllib import error
from urllib import parse
from http import cookiejar
from bs4 import BeautifulSoup
from codeRecognize import getCodeRecognize


def getCurrentWeek(xuehao='0161122147', mima='wl19980805'):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.168 Safari/537.36"
    head = {'User-Agent': user_agent, 'Connection': 'keep-alive'}
    opener = getCodeRecognize(xuehao, mima)
    data_url1 = "http://jwxt.imu.edu.cn/student/rollManagement/electronicRegistration/index"
    req1 = request.Request(url=data_url1, headers=head)
    try:
        response1 = opener.open(req1)
        html = response1.read().decode('utf-8')

        soup = BeautifulSoup(html, "html.parser")

        tim = soup.find_all('a', class_="dropdown-toggle")[0]
        # print(tim)
        ti = str(tim)
        # print("周几：",ti[ti.find("星期")+2])
        # print("第几周：",ti[ti.find("第")+1:ti.find("周")])
        classDay = ti[ti.find("星期")+2]
        classNumber = ti[ti.find("第")+1:ti.find("周")]
        week = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, }
        return classNumber, week[classDay]

    except error.URLError as e:
        if hasattr(e, 'code'):
            print("HTTPError:%d" % e.code)
        elif hasattr(e, 'reason'):
            print("URLError:%s" % e.reason)


if __name__ == '__main__':
    print(getCurrentWeek())
    # getCurrentWeek()

