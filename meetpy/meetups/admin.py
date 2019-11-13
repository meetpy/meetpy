from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html

from . import models


class ExternalLinkInline(admin.TabularInline):
    model = models.ExternalLink
    extra = 1


class TalkInline(admin.StackedInline):
    model = models.Talk
    filter_horizontal = ('speakers',)
    extra = 1


class SponsorInline(admin.TabularInline):
    model = models.MeetupSponsorThrough
    extra = 1
    verbose_name = "sponsor"
    verbose_name_plural = "sponsors"


class MeetupAdmin(admin.ModelAdmin):
    inlines = (SponsorInline, TalkInline, ExternalLinkInline)
    list_display = ("__str__", "date", "venue", "is_ready", "meetup_url_display", "get_absolute_url_display")
    readonly_fields = ('date_modified',)

    @admin.display(description="Meetup URL", ordering="meetup_url")
    def meetup_url_display(self, obj):
        if not obj.meetup_url:
            return None
        return format_html("<a href='{url}'>{url}</a>", url=obj.meetup_url)

    @admin.display(description="Public URL")
    def get_absolute_url_display(self, obj):
        return format_html(
            "<a href='{url}'>{url}</a>",
            url=f"{settings.CONSTANT['GROUP_PAGE_ADDRESS_LONG']}{obj.get_absolute_url()}",
        )


class TalkAdmin(admin.ModelAdmin):
    list_display = ("title", "language", "meetup", "speakers_list", "proposal_date")
    readonly_fields = ["proposal_message", "proposal_date"]
    list_filter = [
        ("meetup", admin.EmptyFieldListFilter),
        ("proposal", admin.EmptyFieldListFilter),
    ]

    @admin.display()
    def proposal_message(self, obj):
        try:
            message = obj.proposal.message
        except IndexError:
            message = ""
        return message

    @admin.display(ordering="proposal__date_submitted")
    def proposal_date(self, obj):
        try:
            date = obj.proposal.date_submitted
        except IndexError:
            date = ""
        return date

    @admin.display()
    def speakers_list(self, obj: "models.Talk"):
        speakers = list(obj.speakers.all())
        if not speakers:
            return None

        return ", ".join(f"{speaker.first_name} {speaker.last_name}" for speaker in speakers)


admin.site.register(models.MeetupType)
admin.site.register(models.Meetup, MeetupAdmin)
admin.site.register(models.Speaker)
admin.site.register(models.Talk, TalkAdmin)
admin.site.register(models.Sponsor)
admin.site.register(models.Venue)
