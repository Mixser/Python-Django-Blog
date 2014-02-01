from django.contrib.auth import authenticate
from django.contrib.auth import login as _login
from django.contrib.auth import logout as _logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from Jiga.forms.edit_user_profile import EditProfileForm

from Jiga.forms.login import LoginForm
from Jiga.forms.post import PostForm
from Jiga.forms.registration import RegistrationForm
from Jiga.models import Post, Comment


def index(request):
    last_recently_posts = Post.objects.all().filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    return render(request, 'Jiga/index.html', {'last_recently_posts': last_recently_posts})


def post(request, post_id):
    _post = get_object_or_404(Post, pk=post_id)
    return render(request, 'Jiga/post.html', {'post': _post})


@login_required
def edit_post(request, post_id):
    _post = get_object_or_404(Post, pk=post_id)
    if _post.user != request.user:
        return HttpResponseRedirect(reverse('jiga:index'))
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            _post.post_title = request.POST['post_title']
            _post.post_text = request.POST['post_text']
            _post.pub_date = request.POST['pub_date']
            _post.save()
            return HttpResponseRedirect(reverse('jiga:post', args=(_post.id,)))

    else:
        form = PostForm(_post.get_date())
        form['pub_date'].css_classes('datepicker')
    return render(request, 'Jiga/post_form.html', {'form': form})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post_title = request.POST['post_title']
            post_text = request.POST['post_text']
            pub_date = request.POST['pub_date']
            user = request.user
            _post = Post(post_title=post_title, post_text=post_text, pub_date=pub_date, user=user)
            _post.save()
            return HttpResponseRedirect(reverse('jiga:post', args=(_post.id, )))
    else:
        form = PostForm()
    return render(request, 'Jiga/post_form.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                _login(request, user)
                return HttpResponseRedirect(reverse('jiga:profile', args=(user.id,)))
            else:
                    return render(request, 'Jiga/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'Jiga/login.html', {'form': form})


def logout(request):
    _logout(request)
    return HttpResponseRedirect(reverse('jiga:index'))


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            user = User(username=username, password=password, email=email,
                        first_name=first_name, last_name=last_name)
            try:
                user.save()   # TODO: validate for multiply user
            except IntegrityError:
                return render(request, 'Jiga/registration.html',
                              {'form': form, 'error_message': 'A user with this name already exists'})
            return HttpResponseRedirect(reverse('jiga:profile', args=(user.id,)))
    else:
        form = RegistrationForm()
    return render(request, 'Jiga/registration.html', {'form': form})


def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'Jiga/profile.html', {'user_': user})

@login_required
def edit_profile(request):
    _user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            _user.first_name = first_name
            _user.last_name = last_name
            _user.save()
            return HttpResponseRedirect(reverse('jiga:profile', args=(_user.id, )))
    else:
        form = EditProfileForm({'first_name': _user.first_name, 'last_name': _user.last_name})
    return render(request, 'Jiga/edit_user_profile.html', {'form': form})



@login_required
def create_comment(request, post_id):
    _post = get_object_or_404(Post, pk=post_id)
    _user = request.user
    if request.method == 'POST':
        comment = Comment(comment_title=request.POST['comment_title'],
                          comment_text=request.POST['comment_text'],
                          post=_post, user=_user,
                          pub_date=timezone.now())
        comment.save()
    return HttpResponseRedirect(reverse('jiga:post', args=(_post.id, ) ))