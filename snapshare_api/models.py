from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# My models.
class Person(models.Model):
    """Is a person with its likes, friends and shared content"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    partner = models.ForeignKey('self', on_delete=models.CASCADE, related_name='partnership')
    likes = models.ManyToManyField('Topic')
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=False)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = 'people'

    def __str__(self):
        return '{} {}'.format(self.user.frist_name, self.user.last_name)

class Friendship(models.Model):
    """The representation of friendship relationship between two people"""
    suitor = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='relations')
    friend = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='fellows')
    hot = models.IntegerField()
    preferences = models.ManyToManyField('Topic')
    start_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return '({!s})-({!s})[{}]'.format(self.suitor, self.friend, self.hot)

class Topic(models.Model):
    """The people's interest"""
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    creator = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='tags')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.slug

class Content(models.Model):
    """The shared content on the page"""
    title = models.CharField(max_length=100)
    post = models.TextField()
    data = models.FileField(upload_to='uploads/', null=True)
    topics = models.ManyToManyField(Topic)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='posts')
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.slug

class Comment(models.Model):
    """Messages about related content or topics"""
    content = models.ForeignKey(Content, related_name='comments')
    tweet = models.CharField(max_length=150)
    owner = models.ForeignKey(Person, related_name='comments')
    related = models.ManyToManyField(Person)

    def __str__(self):
        return self.tweet

class Message(models.Model):
    """The user's messages for chat"""
    user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='chats')
    channel = models.ManyToManyField(Person)
    body = models.TextField()
    attachment = models.FileField(upload_to='attachments/', null=True)

    def __str__(self):
        return self.body
