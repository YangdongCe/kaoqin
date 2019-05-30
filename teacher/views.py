from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from teacher.models import TeacherInfo, teachCourse
from student.models import CourseInfo, SignInfo, StudentCourse
from django.http import HttpResponse
import json
from student.spider3 import getCurrentWeek
from datetime import time
from django.contrib.auth.hashers import make_password, check_password


def tLogin(request):
    return render(request, 'teacher/teacherlogin.html', context={'state':1})


def tRegister(request):
    return render(request, 'teacher/teacherRegister.html')


def tIndex(request):
    return render(request, 'teacher/teacherlogin.html')


def tPage(request):
    tNum = request.session.get('tNum', None)
    tpwd = request.session.get('tPassword')
    # session过期返回登录页面
    if tNum is None or tpwd is None:
        return render(request, 'teacher/teacherlogin.html')
    request.session.set_expiry(60 * 5)  # 5分钟失效
    teacher = TeacherInfo.objects.filter(tNum=tNum)
    if len(teacher) != 0 and tpwd == teacher[0].tPassword:
        tSex = '男' if teacher[0].tSex else '女'
        context = {'tSex': tSex}
        return render(request, 'teacher/teacherpage.html', context)
    else:
        return render(request, 'teacher/teacherlogin.html')


@csrf_protect
@csrf_exempt
def updateSignInfo(request):
    tNum = request.session.get('tNum', None)
    tpwd = request.session.get('tPassword')
    # session过期返回登录页面
    print(tNum, tpwd)
    if tNum is None or tpwd is None:
        return render(request, 'teacher/teacherlogin.html')
    request.session.set_expiry(60 * 5)  # 5分钟失效

    week = ['一', '二', '三', '四', '五', '六', '日']
    cNum = request.POST['cNum']
    cNo = request.POST['cNo']
    cClassDay = request.POST['cClassDay']

    course = CourseInfo.objects.filter(cNum=cNum, cNo=cNo, cClassDay=cClassDay)

    if len(course) != 0:
        signQuery = SignInfo.objects.filter(sCouse=course[0])
        signInfo = []
        for sign in signQuery:
            signInfo.append({'sName': sign.sStudent.sName,
                             'sNum': sign.sStudent.sNum,
                             'sSignTime': sign.sSignTime.strftime('%Y/%m/%d %H:%M:%S'),
                             'cClassWeek': sign.sSignWeek,
                             'cClassDay': week[sign.sSignDay - 1],
                             'state': 1 if sign.sIsSign else 0
                             })
        # context = { signInfo}

        return HttpResponse(json.dumps(signInfo))


def tSignpage(request):
    tNum = request.session.get('tNum', None)
    tpwd = request.session.get('tPassword')
    # session过期返回登录页面
    if tNum is None or tpwd is None:
        return render(request, 'teacher/teacherlogin.html')
    request.session.set_expiry(60 * 5)  # 5分钟失效

    teacher = TeacherInfo.objects.filter(tNum=tNum)
    if len(teacher) != 0 and tpwd == teacher[0].tPassword:
        tSex = '男' if teacher[0].tSex else '女'
        curTimeInfo = getCurrentWeek()
        curWeek = int(curTimeInfo[0])
        curDay = curTimeInfo[1]
        week = ['一', '二', '三', '四', '五', '六', '日']
        tAllCourse = teachCourse.objects.filter(teacher=tNum)
        courseInfo = []
        for tc in tAllCourse:
            if tc.course.cClassWeek[curWeek - 1] == '1' and curDay == tc.course.cClassDay:
                bo = 0
                for j in courseInfo:
                    if (j['cNum'] == str(tc.course.cNum) and j['cNo'] == str(tc.course.cNo) and j['cClassDay'] == '周' +
                            week[
                                tc.course.cClassDay - 1]):
                        bo = 1

                if bo == 1:
                    continue
                courseInfo.append({'cNo': tc.course.cNo,
                                   'cNum': tc.course.cNum,
                                   'cLabel': str(tc.course.cNum) + ',' + str(tc.course.cNo) + ',' + str(
                                       tc.course.cClassDay),
                                   'cName': tc.course.cName,
                                   'cClassDay': '周' + str(week[tc.course.cClassDay - 1])})
            # print(type(tc.course))
        signQuery = SignInfo.objects.filter(sCouse=tAllCourse[0].course)
        signInfo = []
        for sign in signQuery:
            signInfo.append({'sName': sign.sStudent.sName,
                             'sNum': sign.sStudent.sNum,
                             'sSignTime': sign.sSignTime.strftime('%Y/%m/%d %H:%M:%S'),
                             'cClassWeek': sign.sSignWeek,
                             'cClassDay': week[sign.sSignDay - 1],
                             'state': 1 if sign.sIsSign else 0
                             })
        context = {'course': courseInfo, 'signInfo': signInfo, 'tSex': tSex}

        return render(request, 'teacher/teachersignpage.html', context)
    else:
        return render(request, 'teacher/teacherlogin.html')


# 发布签到

@csrf_protect
@csrf_exempt
def tPub(request):
    tNum = request.session.get('tNum', None)
    tpwd = request.session.get('tPassword')
    # session过期返回登录页面
    if tNum is None or tpwd is None:
        return render(request, 'teacher/teacherlogin.html')
    request.session.set_expiry(60 * 5)  # 5分钟失效
    teacher = TeacherInfo.objects.filter(tNum=tNum)
    print(tNum, tpwd)
    print(teacher[0].tPassword)
    if len(teacher) != 0 and tpwd == teacher[0].tPassword:
        tSex = '男' if teacher[0].tSex else '女'
        # 根据用户名查出所有课程
        info = []
        curTimeInfo = getCurrentWeek()
        curWeek = int(curTimeInfo[0])
        curDay = curTimeInfo[1]
        week = ['一', '二', '三', '四', '五', '六', '日']
        # try:
        tAllCourse = teachCourse.objects.filter(teacher=tNum)

        for i in tAllCourse:
            if i.course.cClassWeek[curWeek - 1] == '1' and curDay == i.course.cClassDay:
                bo = 0
                for j in info:
                    if (j['cNum'] == str(i.course.cNum) and j['cNo'] == str(i.course.cNo)
                            and j['cDay'] == '星期' + week[i.course.cClassDay - 1]):
                        bo = 1
                if bo == 1:
                    continue
                info.append({'cNum': str(i.course.cNum),
                             'cNo': str(i.course.cNo),
                             'str': str(i.course.cNum) + str(i.course.cNo)+str(i.course.cClassDay),
                             'cName': i.course.cName,
                             'cLabel': str(i.course.cNum) + ',' + str(i.course.cNo),
                             'cWeek': '第' + str(curWeek) + '周',
                             'cDay': '星期' + week[i.course.cClassDay - 1]})
        # print("info；", info)
        context = {'info': info, 'tSex': tSex}
        return render(request, 'teacher/teacherpubsign.html', context=context)
        # except:
        #     return render(request, 'teacher/teacherpage.html')
    else:
        return render(request, 'teacher/teacherlogin.html')


@csrf_protect
@csrf_exempt
def tSetSign(request):
    tNum = request.session.get('tNum')
    tpwd = request.session.get('tPassword')
    # session过期返回登录页面
    if tNum is None or tpwd is None:
        return render(request, 'teacher/teacherlogin.html')
    request.session.set_expiry(60 * 5)  # 5分钟失效
    # 设置签到，改变签到状态
    cNum = request.POST["cNum"]
    cNo = str(request.POST["cNo"]).zfill(2)
    cBegTime = request.POST["cBegTime"]
    # print(cBegTime)
    # try:
    curTimeInfo = getCurrentWeek()
    curWeek = curTimeInfo[0]
    curDay = curTimeInfo[1]

    ci = CourseInfo.objects.filter(cNum=cNum, cNo=cNo, cClassDay=int(curDay))
    print('ci:', ci, '   ', ci[0].cName)
    sc = []
    for c in ci:
        ss = StudentCourse.objects.filter(course=c)
        print('ss: ', ss)
        sc.append(ss)
    from datetime import time as dtime
    import time
    localTime = time.localtime()
    curTime = dtime(localTime.tm_hour, localTime.tm_min, localTime.tm_sec)
    for st in sc:
        for stu in st:
            si = SignInfo.objects.create(sCouse=ci[0], sStudent=stu.student, sSignDay=curDay, sSignWeek=curWeek,
                                         sSignBegTime=cBegTime, sSignEndTime=stu.course.cEndTime)
            si.save()
    return HttpResponse(json.dumps({'state': '1'}))
    # except :
    #     return HttpResponse(json.dumps({'state': '0'}))


def tLoginInfo(request):
    try:
        tNum = request.POST.get('tNum')
        # print('tid: ', tid)
        tpwd = request.POST.get('pwd')

        # print('Password: ', tpwd)
        tea = TeacherInfo.objects.filter(tNum=tNum)
        # 输入帐号或密码错误
        if len(tea) == 0 or check_password(tpwd, tea[0].tPassword) is False:
            # return  HttpResponse(json.dumps({'state': 0}))
            return render(request, 'teacher/teacherlogin.html', context={'state':0})
        request.session['tNum'] = tNum
        request.session['tPassword'] = tea[0].tPassword
        request.session['tName'] = tea[0].tName
        request.session.set_expiry(60 * 5)  # 5分钟失效

        return redirect("/teacher/tPage")

    except:
        return render(request, 'teacher/teacherlogin.html')


@csrf_protect
@csrf_exempt
def tRegisterInfo(request):
    try:
        cNum = request.POST.get('cNum')
        cNo = request.POST.get('cNo')
        name = request.POST.get('name')
        password = request.POST.get('password')
        sex = request.POST.get('sex')
        tNum = request.POST.get('number')

        if sex == '1':  # 男
            tSex = True
        else:
            tSex = False
        tea = TeacherInfo.objects.create(tNum=tNum, tSex=tSex, tName=name,
                                         tPassword=make_password(password))
        tea.save()
        print(cNum)
        print(cNo)

        # 循环加入teachercourse
        print(cNo.split(','), ' ', len(cNo.split(',')))
        for index in range(len(cNo.split(','))):
            print(index)
            if cNo.split(',')[index] == '':
                break
            cour = CourseInfo.objects.filter(cNum=cNum.split(',')[index], cNo=cNo.split(',')[index])
            # print((list(cour))[0])
            for c in cour:
                tc = teachCourse.objects.create(teacher=tea, course=c)
                tc.save()

        flag = True
    except:
        flag = False
    # 教师注册成功
    if flag == True:
        context = {'flag': 1}
        return HttpResponse(json.dumps(context))
    # 教师注册失败
    else:
        flag = False
        context = {'flag': 0}
        return HttpResponse(json.dumps(context))
