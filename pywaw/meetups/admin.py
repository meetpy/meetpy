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


class TalkProposalAdmin(admin.ModelAdmin):
    readonly_fields = ('talk', 'message', 'date_submitted')
    list_display = ('talk', 'message', 'date_submitted', 'get_meetup')

    def get_meetup(self, obj):
        return obj.talk.meetup

    get_meetup.short_description = 'Meetup'


class TalkAdmin(admin.ModelAdmin):
    list_display = ('title', 'meetup')


admin.site.register(models.Meetup, MeetupAdmin)
admin.site.register(models.Speaker)
admin.site.register(models.Talk, TalkAdmin)
admin.site.register(models.Sponsor)
admin.site.register(models.Venue)
admin.site.register(models.TalkProposal, TalkProposalAdmin)
