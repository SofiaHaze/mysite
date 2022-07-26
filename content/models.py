from django.db import models


# Create your models here.
class Feed(models.Model):
    content = models.TextField()    # 글내용
    image = models.TextField()  # 피드 이미지
    email = models.EmailField(default='')     # 글쓴이
    nickname = models.TextField(default='')


class Like(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    is_like = models.BooleanField(default=True)


class Reply(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    reply_content = models.TextField()


class Bookmark(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    is_marked = models.BooleanField(default=True)


class Weather(models.Model):
    weather =  models.TextField()
    email = models.EmailField(default='')
    content =  models.TextField()

