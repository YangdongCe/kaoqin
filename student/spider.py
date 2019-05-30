import jpype
from jpype import *

jvmPath = './jre/jre/bin/server/jvm.dll'
jarPath = './xuanke2.jar'
jpype,startJVM(jvmPath, "-Djava.class.path=%s" % jarPath)

Jwxt = jpype.JClass('cn.likole.jwxt.Jwxt')
jwxt=Jwxt()
jwxt.login("0161122147","0161122147","error")

CourseParser =jpype.JClass('cn.likole.jwxt.CourseListParser')

a=CourseParser.parse(jwxt.schedule())

"""
courseList:
getProgramPlanCode() 方案计划号
getProgramPlanName() 方案计划名
getTotalUnits() 总学分
getSelectCourseList() 课表
"""

"""
course:
getId() 编号
getUnit() 学分
getCourseName() 课程名
getAttendClassTeacher() 授课教师
getCoursePropertiesCode() 课程属性码
getCoursePropertiesName() 课程属性名
getTimeAndPlaceList() 上课时间
"""

"""
TimeAndPlace :
getClassWeek() 周,例如"111111111111111100000000"
getWeekDescription() 周,例如"1-16周"
getClassDay()  星期
getClassSessions() 节次
getContinuingSession() 节数
getCampusName() 校区,例如"北校区"
getTeachingBuildingName() 教学楼,例如"主楼"
getClassroomName() 教室,例如"307"
"""

"""
id: 
getCoureNumber()
getCoureSequenceNumber()
getExecutiveEducationPlanNumber()
例如：Id{coureNumber='140450490', coureSequenceNumber='01', executiveEducationPlanNumber='2017-2018-2-2'} 
a[0].getSelectCourseList()[i].getId().getCoureNumber()
"""


id = "0161122147"
pwd = "0161122147"
sex = "0"
name = ""
major = a[0].getProgramPlanName()
print("major: ", major)
cid = []
classWeek = []
classDay = []
classSeeion = []
classSeeionContinue = []


"""
第一个循环是有多少门课，
第二课循环是每一门课程一周上几次
"""
for i in range(a[0].getSelectCourseList().size()):
    #Id{coureNumber='140450490', coureSequenceNumber='01', executiveEducationPlanNumber='2017-2018-2-2'} 可以试试变为字典来得到里面的东西
    print(a[0].getSelectCourseList()[i].getCourseName(), " ", a[0].getSelectCourseList()[i].getId(), " ", a[0].getSelectCourseList()[i].getCoursePropertiesCode())
    # sid = a[0].getSelectCourseList()[i].getId()[2:]
    # print(type( a[0].getSelectCourseList()[i].getId()))
    print(a[0].getSelectCourseList()[i].getId().getCoureNumber(),' ',a[0].getSelectCourseList()[i].getId().getCoureSequenceNumber())
    for j in range(a[0].getSelectCourseList()[i].getTimeAndPlaceList().size()):
        p = a[0].getSelectCourseList()[i].getTimeAndPlaceList()[j]
        print(p.getClassWeek(), ' ', p.getClassDay(), ' ', p.getClassSessions(), ' ', p.getContinuingSession())

