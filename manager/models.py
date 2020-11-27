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
            "role": self.role
        }


class Course(models.Model):
    name = models.CharField(max_length=30)
    teacher = models.ForeignKey(to=AppUser, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name}: {self.teacher}"

    @property
    def times(self):
        times = CourseTime.objects.filter(course=self)
        return times

    @property
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "teacher_id": self.teacher_id,
            "times": [x.json for x in self.times]
        }


class CourseTime(models.Model):
    start_week = models.SmallIntegerField()
    end_week = models.SmallIntegerField()
    start_time = models.CharField(max_length=8)
    end_time = models.CharField(max_length=8)
    day = models.SmallIntegerField()
    course = models.ForeignKey(to=Course, on_delete=models.PROTECT)

    def __str__(self):
        return f"{str(self.course.name)}: {self.start_week}-{self.end_week}星期{self.day} {self.start_time}-{self.end_time}"

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
        return f"{str(self.course)} {dict(self.checkin_methods)[self.method]}"


class History(models.Model):
    photographer = models.ForeignKey(to=AppUser, on_delete=models.PROTECT, related_name='photographer_id')
    target = models.ForeignKey(to=AppUser, on_delete=models.PROTECT, null=True, related_name='target_id')
    belong = models.ForeignKey(to=Checkin, on_delete=models.PROTECT)
    image = models.TextField()

    def __str__(self):
        return f"{str(self.belong)} {self.photographer.id}-->{self.target.id}"


class JoinClass(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.PROTECT)
    user = models.ForeignKey(to=AppUser, on_delete=models.PROTECT)

    def __str__(self):
        return f"{str(self.user)} {str(self.course)}"
