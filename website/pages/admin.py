from django.contrib import admin
from pages.models import Media

class MediaAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'showimage']

admin.site.register(Media, MediaAdmin)
