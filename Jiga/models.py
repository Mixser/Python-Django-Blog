import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    user = models.ForeignKey(User)
    post_title = models.CharField(max_length=255)
    post_text = models.TextField()
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.post_title

    def was_published_recently(self):
        now = timezone.now()
        return now > self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def get_date(self):
        return {'post_title': self.post_title,
                'post_text': self.post_text,
                'pub_date': self.pub_date
                }


class Comment(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    comment_title = models.CharField(max_length=255)
    comment_text = models.TextField()
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.comment_title