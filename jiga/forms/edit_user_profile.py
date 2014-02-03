from django import forms

__author__ = 'mixser'


class EditProfileForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()