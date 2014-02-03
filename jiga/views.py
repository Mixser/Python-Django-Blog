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
from jiga.forms.comment import CommentForm
from jiga.forms.edit_user_profile import EditProfileForm
from jiga.forms.login import LoginForm
from jiga.forms.post import PostForm
from jiga.forms.registration import RegistrationForm
from jiga.models import Post, Comment


def index(request):
    last_recently_posts = Post.objects.all().filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    return render(request, 'jiga/index.html', {'last_recently_posts': last_recently_posts})


def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm()
    return render(request, 'jiga/post.html', {'post': post, 'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.user != request.user:
        return HttpResponseRedirect(reverse('jiga:index'))
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post.post_title = form.cleaned_data['post_title']
            post.post_text = form.cleaned_data['post_text']
            post.pub_date = form.cleaned_data['pub_date']
            post.save()
            return HttpResponseRedirect(reverse('jiga:post', args=(post.id,)))

    else:
        form = PostForm(post.get_dict())
        form['pub_date'].css_classes('datepicker')
    return render(request, 'jiga/post_form.html', {'form': form})


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
    return render(request, 'jiga/post_form.html', {'form': form})


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
                    return render(request, 'jiga/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'jiga/login.html', {'form': form})


def logout(request):
    _logout(request)
    return HttpResponseRedirect(reverse('jiga:index'))


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = User(username=username, email=email,
                        first_name=first_name, last_name=last_name)
            user.set_password(password)
            try:
                user.save()   # TODO: validate for multiply user
            except IntegrityError:
                return render(request, 'jiga/registration.html',
                              {'form': form, 'error_message': 'A user with this name already exists'})
            return HttpResponseRedirect(reverse('jiga:profile', args=(user.id,)))
    else:
        form = RegistrationForm()
    return render(request, 'jiga/registration.html', {'form': form})


def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if user == request.user:
        posts = user.post_set.all().order_by('-pub_date')
    else:
        posts = user.post_set.all().filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    return render(request, 'jiga/profile.html', {'user_for_viewing': user, 'posts': posts})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return HttpResponseRedirect(reverse('jiga:profile', args=(user.id, )))
    else:
        form = EditProfileForm({'first_name': user.first_name, 'last_name': user.last_name})
    return render(request, 'jiga/edit_user_profile.html', {'form': form})



@login_required
def create_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_title = form.cleaned_data['comment_title']
            comment_text = form.cleaned_data['comment_text']
            comment = Comment(comment_title=comment_title, comment_text=comment_text,
                              user=user, post=post,pub_date=timezone.now())
            comment.save()
    return HttpResponseRedirect(reverse('jiga:post', args=(post.id, ) ))