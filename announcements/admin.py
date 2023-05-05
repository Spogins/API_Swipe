from django.contrib import admin

from announcements.models import Announcement, Promotion

# Register your models here.
admin.site.register(Announcement)
admin.site.register(Promotion)
