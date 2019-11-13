from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from . import models


class TalkProposalForm(forms.ModelForm):
    talk_title = forms.CharField()
    talk_description = forms.CharField(max_length=1000, widget=forms.Textarea)
    speaker = forms.ModelChoiceField(
        queryset=models.Speaker.objects.filter(talks__meetup__isnull=False).distinct(),
        required=False,
    )
    speaker_first_name = forms.CharField(required=False, max_length=30)
    speaker_last_name = forms.CharField(required=False, max_length=30)
    speaker_website = forms.URLField(required=False)
    speaker_phone = forms.CharField(required=False, max_length=30)
    speaker_email = forms.EmailField(required=False)
    speaker_biography = forms.CharField(required=False, widget=forms.Textarea)
    speaker_photo = forms.ImageField(required=False)
    without_owner = forms.BooleanField(required=False, initial=False)

    REQUIRED_SPEAKER_FIELDS = [
        'speaker_first_name',
        'speaker_last_name',
        'speaker_phone',
        'speaker_email',
        'speaker_biography',
        'speaker_photo',
    ]

    class Meta:
        model = models.TalkProposal
        fields = ('message',)

    def save(self, *args, **kwargs):
        talk_proposal = super().save(commit=False)
        talk = models.Talk.objects.create(
            title=self.cleaned_data['talk_title'],
            description=self.cleaned_data['talk_description'],
        )
        if self.cleaned_data['speaker']:
            speaker = self.cleaned_data['speaker']
        else:
            speaker = models.Speaker.objects.create(
                first_name=self.cleaned_data['speaker_first_name'],
                last_name=self.cleaned_data['speaker_last_name'],
                website=self.cleaned_data['speaker_website'],
                phone=self.cleaned_data['speaker_phone'],
                email=self.cleaned_data['speaker_email'],
                biography=self.cleaned_data['speaker_biography'],
                photo=self.cleaned_data['speaker_photo'],
            )
        talk.speakers.add(speaker)
        talk_proposal.talk = talk
        talk_proposal.save()
        return talk_proposal

    def clean(self):
        if self.cleaned_data['without_owner'] is False and self._existing_speaker_field_empty():
            if self._all_required_new_speaker_fields_empty():
                raise ValidationError(settings.CONSTANT['EITHER_EXISTING_OR_NEW_SPEAKER_ERROR'])
            elif not self._all_required_new_speaker_fields_empty():
                for field_name in self.REQUIRED_SPEAKER_FIELDS:
                    if self.cleaned_data.get(field_name) in ['', None]:
                        self._errors[field_name] = self.fields[field_name].error_messages['required']
        return self.cleaned_data

    def _all_required_new_speaker_fields_empty(self):
        return all(self.cleaned_data.get(field_name) == '' for field_name in self.REQUIRED_SPEAKER_FIELDS)

    def _existing_speaker_field_empty(self):
        return not self.cleaned_data['speaker']
