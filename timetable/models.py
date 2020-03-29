from django.db import models

# Create your models here.
class user_info(models.Model):
    user = models.CharField(max_length=9)
    pwd = models.CharField(max_length=32)
    times = models.CharField(max_length=3, default='0')

class all_lesson(models.Model):

    lesson = models.CharField(max_length=32) #课程名称
    teacher = models.CharField(max_length=32) #上课老师
    location = models.CharField(max_length=32) # 上课地点
    classes = models.CharField(max_length=32) #上课班级
    credit = models.CharField(max_length=8) #学分
    user = models.CharField(max_length=32) #关联学生
# class timetable(models.Model)

class lesson_info(models.Model):
    user = models.CharField(max_length=32, default="")
    info = models.CharField(max_length=256)


    # def __str__(self):
    #     return self.name