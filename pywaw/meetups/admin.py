from django.contrib import admin
from . import models

admin.site.register(models.Meetup)
admin.site.register(models.Speaker)
admin.site.register(models.Talk)
admin.site.register(models.Sponsor)
