from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from student import spider2
from urllib import request as req0
from urllib import error
from urllib import parse
from http import cookiejar
import json
from student.validFace import detectiveFace,image_to_base64
from student import util
from student.models import FaceInfo, StudentInfo, CourseInfo,StudentCourse,SignInfo
from student.util import computeDistince
from student.spider3 import getCurrentWeek
from datetime import datetime
import os
from django.contrib.auth.hashers import make_password, check_password

login_url = "http://jwxt.imu.edu.cn/j_spring_security_check"
user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.168 Safari/537.36"
head = {'User-Agent': user_agent, 'Connection':'keep-alive'}

from django.views.decorators.csrf import csrf_protect, csrf_exempt

imageData = ""
limageData = ""

def index(request):
    return render(request, "home.html")

def sLogin(request):
    return render(request, 'student/studentLogin.html')

def sRegister(request):
    return render(request, 'student/studentRegister.html')

def sPage(request):
    sNum=request.session.get('studentId')
    # sPwd = request.session.get('spwd')
    # print(sNum,sPwd)
    if sNum is not None:
        stu=StudentInfo.objects.get(sNum=sNum)
        # if check_password(sPwd,stu.sPassword):
        sName=stu.sName
        sSex='男' if stu.sSex else '女'
        request.session.delete('studentId')

        request.session['studentId']=sNum
        request.session['password'] = stu.sPassword
        request.session.set_expiry(300)
        context={'sName':sName,'sNum':sNum,'sSex':sSex}
        return render(request, 'student/studentpage.html',context)
    else:
        return render(request, 'student/404.html')


@csrf_protect
@csrf_exempt
def sRegisterInfo(request):

    sid = request.POST['number']

    if 1 == 1:

        spwd = request.POST['pwd']
        gender = request.POST['gender']
        #name, gender, xi, zhuanye, banji

        #用爬虫2得到名字，性别， 系，专业， 班级 例如：('王磊', '男', '软件工程系', '软件工程', '软件工程16级1班')
        name, gender2 , syst, major, grade = spider2.getMessage2(sid, spwd)
        print(name, gender2 , syst, major, grade)
        # sNum, sName, sSex, sPassword, sMajor, sGrade 保存个人信息
        if gender2 == "男":
            gen = True
        else:
            gen = False
        stu = StudentInfo.objects.create(sNum=sid, sName=name, sSex=gen,
                                         sPassword=make_password(spwd),
                                         sMajor=major, sGrade=grade)
        stu.save()

        saveBaseFeature = request.session['saveBaseFeature']
        print("id: ",id)
        face = FaceInfo.objects.create(feature=saveBaseFeature,student_id=sid)
        face.save()

        #用爬虫1得到课程信息
        login_data = {}
        login_data['j_username'] = sid
        login_data['j_password'] = spwd
        login_data['j_captcha1'] = 'error'

        loginpostdata = parse.urlencode(login_data).encode('utf-8')

        cookie = cookiejar.CookieJar()
        cookie_support = req0.HTTPCookieProcessor(cookie)
        opener = req0.build_opener(cookie_support)

        req = req0.Request(url=login_url, data=loginpostdata, headers=head)

        data_url1 = "http://jwxt.imu.edu.cn/student/courseSelect/thisSemesterCurriculum/ajaxStudentSchedule/callback"
        # data_data1 = {}
        # data_data1['ff'] = 'f'
        # data_data1['planNumber'] = ''
        req1 = req0.Request(url=data_url1, headers=head)

        try:
            response = opener.open(req)
            response1 = opener.open(req1)
            html = response1.read().decode('utf-8')

            js = json.loads(html)
            print(js['dateList'][0]['programPlanName'])

            # 可以看有几门课程 10
            print('一周几门： ', len(js['dateList'][0]['selectCourseList']))
            # 可以得到这门课程一周有几节
            print('一周几节：', len(js['dateList'][0]['selectCourseList'][2]['timeAndPlaceList']))
            for j in range(len(js['dateList'][0]['selectCourseList'])):
                try:
                    js['dateList'][0]['selectCourseList'][j]['timeAndPlaceList']
                except:
                    continue
                for i in range(len(js['dateList'][0]['selectCourseList'][j]['timeAndPlaceList'])):
                    coureName = js['dateList'][0]['selectCourseList'][j]['timeAndPlaceList'][i]['coureName']
                    classWeek = js['dateList'][0]['selectCourseList'][j]['timeAndPlaceList'][i]['classWeek']
                    coureNumber = js['dateList'][0]['selectCourseList'][j]['timeAndPlaceList'][i]['coureNumber']
                    coureSequenceNumber = js['dateList'][0]['selectCourseList'][j]['timeAndPlaceList'][i]['coureSequenceNumber']
                    classSessions = js['dateList'][0]['selectCourseList'][j]['timeAndPlaceList'][i]['classSessions']
                    continuingSession = js['dateList'][0]['selectCourseList'][j]['timeAndPlaceList'][i]['continuingSession']
                    classDay = js['dateList'][0]['selectCourseList'][j]['timeAndPlaceList'][i]['classDay']
                    #这里应该保存了
                    #self, cId, cNum, cName, cMajor, cClassWeek, cClassDay,cClassSessions, cContinuingSession
                    # print(int(classSessions),' ', int(continuingSession))
                    cour = CourseInfo.objects.create(cNum=coureNumber, cNo=coureSequenceNumber, cName=coureName, cMajor="暂无", cClassWeek=classWeek,
                                                     cClassDay=int(classDay), cClassSessions=int(classSessions), cContinuingSession=int(continuingSession))
                    cour.save()
                    """
                    插入选课信息
                  """
                    # self, studentID, courseID  StudentCourse
                    # ci = CourseInfo()
                    # ccid = CourseInfo.objects.get(cNum=coureNumber,cNo=coureSequenceNumber)
                    # print('cdid: ',ccid,' ' ,type(ccid))

                    sc = StudentCourse.objects.create(studentID=stu, courseID=cour)
                    sc.save()

        except error.URLError as e:
            print("错误")
            return render(request, 'student/studentRegister.html')
        return redirect('/student/sLogin')
    else:
        return render(request, 'student/studentRegister.html')

@csrf_protect
@csrf_exempt
def sLoginInfo(request):

    sNum = request.POST['number']
    sPwd = request.POST['pwd']
    stu = StudentInfo.objects.filter(sNum=sNum )
    if len(stu) != 0 and check_password(sPwd,stu[0].sPassword):
        request.session['studentId'] = stu[0].sNum
        request.session['spwd'] = stu[0].sPassword
        request.session.set_expiry(300)
        # state = True
    # if True==state:
        """这里要查出个人信息，放入session中"""
        # request.session[] =
        # set_expiry方法是设置session
        # 前端用request.session.属性

        context = {'flag':1}
        return render(request, "student/studentpage.html", context=context)
        # return redirect('/student/sLoginInfo')

    else:
        return render(request, 'student/studentLogin.html')






def sSignPage(request):
    """
    这里也要查出要签到的课程，还有个人信息
    :param request:
    :return:
    """
    studentId = request.session.get('studentId')
    sPassword= request.session.get('password')
    # 前端判断状态码

    if studentId != '' and sPassword !='':
        stu = StudentInfo.objects.get(sNum=studentId)
        if sPassword == stu.sPassword:
            curTimeInfo=getCurrentWeek(studentId,sPassword)
            curWeek=int(curTimeInfo[0])
            curDay=curTimeInfo[1]
            sName = stu.sName
            sSex = '男' if stu.sSex else '女'
            signInfo=SignInfo.objects.filter(sStudent=stu)

            courseInfoList=[]
            for sign in signInfo:
                course=sign.sCouse
                classWeek=course.cClassWeek
                classDay=course.cClassDay
                state = 1 if sign.sIsSign else 0
                if classWeek[curWeek-1]=='1' and curDay==classDay:
                    courseInfoList.append({'cNum':course.cNum,
                                           'cNo':course.cNo,
                                           'cName':course.cName,
                                           'cClassDay': course.cClassDay,
                                           'sSignBegTime':datetime.now().strftime('%Y/%m/%d')+'  '+sign.sSignBegTime.strftime('%H:%M:%S'),
                                           'sSignEndTime': datetime.now().strftime( '%Y/%m/%d') + '  ' + sign.sSignEndTime.strftime('%H:%M:%S'),
                                           'sState':state})
                # print(courseInfoList)

            # print(courseInfoList)
            request.session.set_expiry(300)
            context = {'sName': sName, 'sNum': studentId, 'sSex': sSex,'couseInfo':courseInfoList}
            return render(request, 'student/studentSignpage.html',context)
    else:
        return render(request, 'student/404.html')

    # return render(request, 'student/studentSignpage.html')

def sSingInfo(request):
    """
    从数据库里查出签到记录放入content中，还有个人信息
    :param request:
    :return:
    """

    studentId = request.session.get('studentId')
    sPassword = request.session.get('password')
    stu = StudentInfo.objects.get(sNum=studentId, sPassword=sPassword)

    info=[]
    signInfo = SignInfo.objects.filter(sStudent=stu)
    for sign in signInfo:
        info.append({'cName':sign.sCouse.cName,'sSignTime':sign.sSignTime.strftime('%Y/%m/%d %H:%M:%S'),
                     'state':1 if sign.sIsSign else 0})
    sex='男' if stu.sSex else '女'
    context = {'signInfo':info,'sName':stu.sName,'sSex':sex}

    return render(request, "student/studentSigninfolist.html",context)

@csrf_protect
@csrf_exempt
def sSetSign(request):

    studentId = request.session.get('studentId')
    sPassword = request.session.get('password')
    print(studentId,sPassword)
    # try:
    from datetime  import time as dtime
    import time
    cClassDay=request.POST.get('cClassDay')
    cNum=request.POST.get('cNum')
    cNo =str(request.POST.get('cNo')).zfill(2)
    course=CourseInfo.objects.filter(cNum=cNum,cNo=cNo,cClassDay=cClassDay)
    stu = StudentInfo.objects.get(sNum=studentId,sPassword=sPassword)
    signInfo=SignInfo.objects.get(sCouse=course[0],sStudent=stu)
    localTime=time.localtime()
    curTime = dtime(localTime.tm_hour,localTime.tm_min,localTime.tm_sec)
    if 1==1:
    # if curTime > signInfo.sSignBegTime and curTime < signInfo.sSignEndTime:
        signInfo.sIsSign = True
        signInfo.save()
        state = {'state': 1}
        return HttpResponse(json.dumps(state), content_type="application/json")
    else:
        state = {'state': 0}
        return HttpResponse(json.dumps(state), content_type="application/json")
    # except:
    #     state = {'state': 0}
    #     return HttpResponse(json.dumps(state), content_type="application/json")

@csrf_protect
@csrf_exempt
def srImage(request):
    imageData = request.POST['imageData']
    try:
        # print(type(imageData))
        res = detectiveFace(imageData)
        flag= True if res['state']==1 else False
    except ConnectionError:
        print("ConnectionError")
        sta = {'state': 0}
        return HttpResponse(json.dumps(sta))
    if flag:
        sta = {'state': 1}
        baseFeature = util.getFaceFeature(res['imgBase64'])
        import numpy as np

         # *********************** /加入到数据库中***********"
        id = request.POST['id']
        # print("id type",type(id))
        saveBaseFeature=json.dumps({'face':(np.fromstring(baseFeature,dtype=float).tolist())})
        # print(type(saveBaseFeature))
        # face = FaceInfo.objects.create(feature=saveBaseFeature,student_id=id)
        # face.save()
        request.session['saveBaseFeature'] = saveBaseFeature
        request.session.set_expiry(0)
        return HttpResponse(json.dumps(sta))
    else:
        sta = {'state': 0}
        return HttpResponse(json.dumps(sta))

# 0161122147
@csrf_protect
@csrf_exempt
def sLoginImage(request):
    if 'imageData' in request.POST.keys():

        imageData = request.POST['imageData']
        res=detectiveFace(imageData)
        if res['state']==1:
            import numpy as np
            currentFeature = util.getFaceFeature(res['imgBase64'])
            faceAll=FaceInfo.objects.all()
            minStudentID=''
            minFeatureStr=''
            minDistance=99999.0
            for face in faceAll:
                faceJson=json.loads(face.feature)
                faceStr=np.array(faceJson['face']).tostring()
                curDistance=computeDistince(currentFeature,faceStr)
                print("curDistance:",curDistance)
                if curDistance<minDistance:
                    minDistance=curDistance
                    minStudentID=face.student_id
                    minFeatureStr=minFeatureStr
            print(minDistance)
            if minDistance<1.0:
                state = {'state':1}
                request.session['studentId']=minStudentID
                request.session.set_expiry(300)

                return HttpResponse(json.dumps(state), content_type="application/json")

        state = {'state': 0}
        return HttpResponse(json.dumps(state), content_type="application/json")
