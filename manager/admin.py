from django.contrib import admin
from manager.models import *


class ManagerAdmin(admin.ModelAdmin):
    pass


admin.site.register(AppUser, ManagerAdmin)
admin.site.register(Course, ManagerAdmin)
admin.site.register(CourseTime, ManagerAdmin)
admin.site.register(Checkin, ManagerAdmin)
admin.site.register(History, ManagerAdmin)
admin.site.register(JoinClass, ManagerAdmin)
