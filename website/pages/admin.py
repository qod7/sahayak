from django.contrib import admin
from pages.models import Media,Field,WorkerInfo,Job,UserInfo

class MediaAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'showimage']

admin.site.register(Media, MediaAdmin)


class FieldAdmin(admin.ModelAdmin):
    pass

admin.site.register(Field, FieldAdmin)


class WorkerInfoAdmin(admin.ModelAdmin):
    pass

admin.site.register(WorkerInfo, WorkerInfoAdmin)


class JobAdmin(admin.ModelAdmin):
    pass

admin.site.register(Job, JobAdmin)


class UserInfoAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserInfo, UserInfoAdmin)