from django import forms
from . import models


class TalkProposalForm(forms.Form):
    talk_title = forms.CharField()
    talk_description = forms.CharField(max_length=1000, widget=forms.Textarea)
    speaker = forms.ModelChoiceField(queryset=models.Speaker.objects.all(), required=False)
    speaker_first_name = forms.CharField(required=False, max_length=30)
    speaker_last_name = forms.CharField(required=False, max_length=30)
    speaker_website = forms.URLField(required=False)
    speaker_phone = forms.CharField(required=False, max_length=30)
    speaker_email = forms.EmailField(required=False)
    speaker_biography = forms.CharField(required=False)
    speaker_photo = forms.ImageField(required=False)
