from django import forms


class CommentForm(forms.Form):
    comment_title = forms.CharField()
    comment_text = forms.CharField(widget=forms.Textarea)


class EditProfileForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class PostForm(forms.Form):
    post_title = forms.CharField()
    post_text = forms.CharField(widget=forms.Textarea)
    pub_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'id': 'datepicker'}))

    class Media(object):
        js = ('jiga/js/datepicker.js', )


class RegistrationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
