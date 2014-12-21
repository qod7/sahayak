from django.contrib import admin
from pages.models import Media,Field,WorkerInfo

class MediaAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'showimage']

admin.site.register(Media, MediaAdmin)


class FieldAdmin(admin.ModelAdmin):
    pass

admin.site.register(Field, FieldAdmin)


class WorkerInfoAdmin(admin.ModelAdmin):
    pass

admin.site.register(WorkerInfo, WorkerInfoAdmin)
