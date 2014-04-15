from django import forms


class TalkProposalForm(forms.Form):
    talk_title = forms.CharField()
    talk_description = forms.CharField(max_length=1000)
    speaker_id = forms.IntegerField(required=False)
    speaker_first_name = forms.CharField(required=False, max_length=30)
    speaker_last_name = forms.CharField(required=False, max_length=30)
    speaker_website = forms.URLField(required=False)
    speaker_phone = forms.CharField(required=False, max_length=30)
    speaker_email = forms.EmailField(required=False)
    speaker_biography = forms.CharField(required=False)
