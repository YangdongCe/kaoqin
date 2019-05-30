from django.db import models
from datetime import time

class StudentManager(models.Manager):
    def create(self, sNum, sName, sSex, sPassword, sMajor, sGrade):
        stu = StudentInfo()
        stu.sNum = sNum
        stu.sName = sName
        stu.sSex = sSex
        stu.sPassword = sPassword
        stu.sMajor = sMajor
        stu.sGrade = sGrade
        return stu
class StudentInfo(models.Model):
    sNum = models.CharField(max_length=10, primary_key=True)
    sName = models.CharField(max_length=30)
    sSex = models.BooleanField()
    sPassword = models.CharField(max_length=100)
    sMajor = models.CharField(max_length=50)
    sGrade = models.CharField(max_length=10)

    class Meta():
        db_table = 'student'

    def __str__(self):
        return self.sName

    objects = StudentManager()

class CourseManager(models.Manager):

    def create(self, cNo, cNum, cName, cMajor, cClassWeek, cClassDay,cClassSessions, cContinuingSession):
        cou = CourseInfo()
        cou.cNo = cNo
        cou.cNum = cNum
        cou.cName = cName
        cou.cMajor = "暂无"
        cou.cClassWeek = cClassWeek
        cou.cClassDay = cClassDay
        cou.cClassSessions=cClassSessions
        cou.cContinuingSession = cContinuingSession

        return cou

    # cou=CourseInfo.objects.create('140462620','01','编程实践','software','11111111111100000000',1,1,2)

class CourseInfo(models.Model):
    # 课程号
    cNum = models.CharField(max_length=15)
    # 课序号
    cNo = models.CharField(max_length=4)
    cName = models.CharField(max_length=30)
    cMajor = models.CharField(max_length=50)
    cClassWeek = models.CharField(max_length=25)
    cClassDay = models.IntegerField()
    cClassSessions = models.IntegerField()
    cContinuingSession = models.IntegerField()
    cBegTime = models.TimeField(blank=True)
    cEndTime = models.TimeField(blank=True)

    class Meta():
        db_table = 'course'
        # 设置联合主键 (课程号,课序号)
        # unique_together = (('cNum', 'cNo'))

    # def __str__(self):
    #     return self.cName

    def save(self,*args,**kwargs):
        cBegTimeList = [
            time(8, 0, 0),
            time(9, 0, 0),
            time(10, 10, 0),
            time(11, 10, 0),
            time(14, 30, 0),
            time(15, 30, 0),
            time(16, 40, 0),
            time(17, 40, 0),
            time(19, 0, 0),
            time(20, 0, 0),
            time(21, 0, 0)]
        cEndTimeList = [
            time(8, 50, 0),
            time(9, 50, 0),
            time(11, 0, 0),
            time(12, 0, 0),
            time(15, 20, 0),
            time(16, 20, 0),
            time(17, 30, 0),
            time(18, 30, 0),
            time(19, 50, 0),
            time(20, 50, 0),
            time(21, 50, 0)]
        self.cBegTime=cBegTimeList[self.cClassSessions-1]
        self.cEndTime = cEndTimeList[self.cClassSessions+self.cContinuingSession - 2]

        return super(CourseInfo,self).save(*args,**kwargs)

    objects = CourseManager()

class SCManager(models.Manager):
    def create(self, studentID, courseID):
        sc = StudentCourse()
        sc.student = studentID
        sc.course = courseID
        return sc

class StudentCourse(models.Model):
    student = models.ForeignKey('StudentInfo')
    course = models.ForeignKey('CourseInfo')
    score = models.IntegerField(null=True,blank=True)
    class Meta():
        db_table = 'studentcourse'
        # unique_together = (('student', 'course'))

    objects = SCManager()

class FaceInfo(models.Model):
    # faceID = models.IntegerField(primary_key=True, auto_created=True)
    feature = models.TextField(max_length=1050)
    student = models.OneToOneField('StudentInfo')

    class Meta():
        db_table = 'faceInfo'

class SignManager(models.Manager):
    def create(self,sCouse,sStudent):
        sign=SignInfo()
        sign.sCouse=sCouse
        sign.sStudent=sStudent
        return sign
class SignInfo(models.Model):
    sSignTime = models.DateTimeField(auto_now=True,null=True,blank=True)
    sIsSign = models.BooleanField(default=False)
    sSignDay=models.IntegerField(default=1)
    sSignWeek=models.IntegerField(default=10)
    sSignBegTime=models.TimeField(default=time(8, 30, 0))
    sSignEndTime = models.TimeField(default=time(14, 30, 0))
    sCouse = models.ForeignKey('CourseInfo', blank=True)
    sStudent = models.ForeignKey('StudentInfo', blank=True)

    class Meta():
        db_table = 'signInfo'

