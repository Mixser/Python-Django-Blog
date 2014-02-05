
from django.conf.urls import patterns, include, url

from django.contrib import admin

from jiga import views


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<post_id>\d+)$', views.post, name='post'),
    url(r'^post/(?P<post_id>\d+)/edit$', views.edit_post, name='edit_post'),
    url(r'^profile/(?P<user_id>\d+)$', views.profile, name='profile'),
    url(r'^profile/(?P<user_id>\d+)/follow$', views.follow, name='follow'),
    url(r'^profile/(?P<user_id>\d+)/unfollow$', views.unfollow, name='unfollow'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^new_post/', views.create_post, name='create_post'),
    url(r'^profile/edit', views.edit_profile, name='edit_profile'),
    url(r'^create_comment/(?P<post_id>\d+)$', views.create_comment, name='create_comment')

)
