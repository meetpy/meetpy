from django.contrib import admin
from . import models


class ExternalLinkInline(admin.TabularInline):
    model = models.ExternalLink
    extra = 1


class TalkInline(admin.StackedInline):
    model = models.Talk
    filter_horizontal = ('speakers',)
    extra = 1


class MeetupAdmin(admin.ModelAdmin):
    inlines = (TalkInline, ExternalLinkInline)
    readonly_fields = ('date_modified',)

admin.site.register(models.Meetup, MeetupAdmin)
admin.site.register(models.Speaker)
admin.site.register(models.Talk)
admin.site.register(models.Sponsor)
admin.site.register(models.Venue)
