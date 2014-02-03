from django import forms

__author__ = 'mixser'


class CommentForm(forms.Form):
    comment_title = forms.CharField()
    comment_text = forms.CharField(widget=forms.Textarea)
