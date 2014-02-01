from django import forms
__author__ = 'mixser'


class PostForm(forms.Form):
    post_title = forms.CharField()
    post_text = forms.CharField(widget=forms.Textarea)
    pub_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'id': 'datepicker'}))