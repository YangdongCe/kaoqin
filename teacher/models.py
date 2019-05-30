from django.db import models
from student.models import CourseInfo

# class TeacherManager(models.Manager):
#     def create(self,tNum,):
#         pass
class TeacherInfo(models.Model):
    tNum=models.CharField(max_length=10,primary_key=True)
    tName=models.CharField(max_length=30)
    tSex=models.BooleanField()
    tPassword=models.CharField(max_length=100)
    class Meta():
        db_table='teacher'
    def __str__(self):
        return self.tName

class teachCourseManager(models.Manager):
    def create(self,course , teacher):
        tc = teachCourse()
        tc.course = course
        tc.teacher = teacher
        return tc

class teachCourse(models.Model):
    teacher=models.ForeignKey(TeacherInfo)
    course=models.ForeignKey(CourseInfo)
    objects = teachCourseManager()
    class Meta():
        db_table='teacherCourse'
        unique_together = ('teacher', 'course')

