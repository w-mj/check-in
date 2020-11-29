from django.db import models
from django.contrib.auth.models import User
import json


class AppUser(models.Model):
    id = models.CharField(db_index=True, null=False, max_length=30, primary_key=True)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    image = models.TextField(null=True, blank=True)
    role = models.SmallIntegerField(choices=[(0, '教师'), (1, '学生')])

    def __str__(self):
        return f"{self.id} {self.name} {'学生' if self.role else '教师'}"

    @property
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "image": self.image,
            "token": self.id
        }


class Course(models.Model):
    name = models.CharField(max_length=30)
    teacher = models.ForeignKey(to=AppUser, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.id} {self.name}: {self.teacher}"

    @property
    def time(self):
        times = CourseTime.objects.filter(course=self)
        return times

    @property
    def json(self):
        last_check = Checkin.objects.filter(course=self).order_by('-id')
        return {
            "id": self.id,
            "name": self.name,
            "teacher_id": self.teacher_id,
            "time": [x.json for x in self.time],
            "checking": len(last_check) != 0 and last_check.first().end_time is None
        }


class CourseTime(models.Model):
    start_week = models.SmallIntegerField()
    end_week = models.SmallIntegerField()
    start_time = models.CharField(max_length=8)
    end_time = models.CharField(max_length=8)
    day = models.SmallIntegerField()
    course = models.ForeignKey(to=Course, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.id} {str(self.course.name)}: {self.start_week}-{self.end_week}星期{self.day} {self.start_time}-{self.end_time}"

    @property
    def json(self):
        return {
            "start_week": self.start_week,
            "end_week": self.end_week,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "day": self.day
        }


class Checkin(models.Model):
    checkin_methods = [
        (1, '自拍'),
        (2, '拍别人'),
        (3, '被别人拍'),
        (4, '拍老师')
    ]
    course = models.ForeignKey(to=Course, on_delete=models.PROTECT)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    method = models.SmallIntegerField(choices=checkin_methods)
    count = models.SmallIntegerField(default=1)

    def __str__(self):
        return f"{self.id} {str(self.course)} {dict(self.checkin_methods)[self.method]}"

    def result(self):
        his = History.objects.filter(belong=self)
        res = [(x.photographer_id, x.target_id, x) for x in his]
        res_filter = {
            1: lambda x: x[0] == x[1],
            2: lambda x: x[0] != x[1],
            3: lambda x: x[0] != x[1],
            4: lambda x: x[1] == self.course.teacher_id
        }
        res = [x for x in res if res_filter[self.method](x)]
        stu_id_lst = [x.user_id for x in JoinClass.objects.filter(course=self.course)]
        cnt_photos = {x: 0 for x in stu_id_lst}
        cnt_photos_by = {x: 0 for x in stu_id_lst}
        for x in res:
            cnt_photos[x[0]] += 1
            cnt_photos_by[x[1]] += 1
        suc_filter = {
            1: lambda x: cnt_photos[x] >= 1,
            2: lambda x: cnt_photos[x] >= self.count,
            3: lambda x: cnt_photos_by[x] >= self.count,
            4: lambda x: cnt_photos[x] >= 1
        }
        stu_sec = [(x, suc_filter[self.method](x)) for x in stu_id_lst]
        return [x[2] for x in res], stu_sec


class History(models.Model):
    photographer = models.ForeignKey(to=AppUser, on_delete=models.PROTECT, related_name='photographer_id')
    target = models.ForeignKey(to=AppUser, on_delete=models.PROTECT, null=True, related_name='target_id')
    belong = models.ForeignKey(to=Checkin, on_delete=models.PROTECT)
    image = models.TextField()

    def __str__(self):
        return f"{self.id} ({str(self.belong)}) {self.photographer.id}-->{self.target.id}"

    @property
    def json(self):
        return {
            'photographer_id': self.photographer.id,
            'photographer_name': self.photographer.name,
            'target_id': self.target.id,
            'target_name': self.target.name
        }


class JoinClass(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.PROTECT)
    user = models.ForeignKey(to=AppUser, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.id} {str(self.user)} {str(self.course)}"
