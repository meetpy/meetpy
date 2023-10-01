from django.conf import settings
from django.contrib import admin
from django.contrib.admin.widgets import AdminTextareaWidget
from django.forms import ModelForm, TextInput
from django.utils.html import format_html

from . import models


class AdminMarkdownWidget(AdminTextareaWidget):
    def __init__(self, attrs=None):
        super().__init__(
            attrs={
                'class': 'vLargeTextField wysiwygEditor wysiwygEditor-allowDark',
                **(attrs or {}),
            },
        )

    class Media:
        css = {
            "all": ["css/toastui-editor.min.css", "css/toastui-editor-dark.min.css"],

        }
        js = ["js/toastui-editor-all.min.js", "js/wysiwygEditor.js"]


class ExternalLinkInlineForm(ModelForm):
    class Meta:
        model = models.ExternalLink
        widgets = {
            "description": TextInput(attrs={"class": "vTextField"}),
        }
        exclude = []


class ExternalLinkInline(admin.TabularInline):
    model = models.ExternalLink
    extra = 1
    form = ExternalLinkInlineForm


class TalkInlineForm(ModelForm):
    class Meta:
        model = models.Talk
        widgets = {
            "description": AdminMarkdownWidget(),
        }
        exclude = []


class TalkInline(admin.StackedInline):
    model = models.Talk
    filter_horizontal = ('speakers',)
    extra = 1
    form = TalkInlineForm


class SponsorInlineForm(ModelForm):
    class Meta:
        model = models.Talk
        widgets = {
            "meetup_description": AdminMarkdownWidget(),
        }
        exclude = []


class SponsorInline(admin.TabularInline):
    model = models.MeetupSponsorThrough
    extra = 1
    verbose_name = "sponsor"
    verbose_name_plural = "sponsors"
    form = SponsorInlineForm


class MeetupAdminForm(ModelForm):
    class Meta:
        model = models.Meetup
        widgets = {
            "description": AdminMarkdownWidget(),
        }
        exclude = []


class MeetupAdmin(admin.ModelAdmin):
    inlines = (SponsorInline, TalkInline, ExternalLinkInline)
    list_display = ("__str__", "date", "venue", "is_ready", "meetup_url_display", "get_absolute_url_display")
    readonly_fields = ('date_modified',)
    form = MeetupAdminForm

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


class SpeakerAdminForm(ModelForm):
    class Meta:
        model = models.Talk
        widgets = {
            "biography": AdminMarkdownWidget(),
        }
        exclude = []


class SpeakerAdmin(admin.ModelAdmin):
    form = SpeakerAdminForm


class TalkAdminForm(ModelForm):
    class Meta:
        model = models.Talk
        widgets = {
            "description": AdminMarkdownWidget(),
        }
        exclude = []


class TalkAdmin(admin.ModelAdmin):
    list_display = ("title", "language", "meetup", "speakers_list", "proposal_date")
    readonly_fields = ["proposal_message", "proposal_date"]
    list_filter = [
        ("meetup", admin.EmptyFieldListFilter),
        ("proposal", admin.EmptyFieldListFilter),
    ]
    form = TalkAdminForm

    @admin.display()
    def proposal_message(self, obj):
        try:
            message = obj.proposal.message_md
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


class SponsorAdminForm(ModelForm):
    class Meta:
        model = models.Talk
        widgets = {
            "description": AdminMarkdownWidget(),
        }
        exclude = []


class SponsorAdmin(admin.ModelAdmin):
    form = SponsorAdminForm


admin.site.register(models.MeetupType)
admin.site.register(models.Meetup, MeetupAdmin)
admin.site.register(models.Speaker, SpeakerAdmin)
admin.site.register(models.Talk, TalkAdmin)
admin.site.register(models.Sponsor, SponsorAdmin)
admin.site.register(models.Venue)
