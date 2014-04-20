from django import forms
from . import models
from django.core.exceptions import ValidationError
from meetups.constants import EITHER_EXISTING_OR_NEW_SPEAKER_ERROR


class TalkProposalForm(forms.Form):
    talk_title = forms.CharField()
    talk_description = forms.CharField(max_length=1000, widget=forms.Textarea)
    speaker = forms.ModelChoiceField(queryset=models.Speaker.objects.all(), required=False)
    speaker_first_name = forms.CharField(required=False, max_length=30)
    speaker_last_name = forms.CharField(required=False, max_length=30)
    speaker_website = forms.URLField(required=False)
    speaker_phone = forms.CharField(required=False, max_length=30)
    speaker_email = forms.EmailField(required=False)
    speaker_biography = forms.CharField(required=False, widget=forms.Textarea)
    speaker_photo = forms.ImageField(required=False)

    def clean(self):
        if self.all_new_speaker_fields_empty() and self.existing_speaker_field_empty():
            raise ValidationError(EITHER_EXISTING_OR_NEW_SPEAKER_ERROR)
        return self.cleaned_data

    def all_new_speaker_fields_empty(self):
        is_new_speaker_field = lambda f: f.startswith('speaker_')
        return all([not v for k, v in self.cleaned_data.items() if is_new_speaker_field(k)])

    def existing_speaker_field_empty(self):
        return self.cleaned_data['speaker'] is None
