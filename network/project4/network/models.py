from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
from django.utils import timezone

class User(AbstractUser):
    pass


    
class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, default='Name Edit Here' )
    bio = models.TextField(max_length=500,  default='Edit Bio Here')
    birth_date = models.DateField(null=True, blank=True, default='1900-01-01')
    location = models.CharField(max_length=100, blank=True, null=True, default='Location you live?')
    # picture = models.ImageField(upload_to='uploads/profile_pictures/', default='uploads/profile_pictures/default.png', blank=True)
    following = models.ManyToManyField(User, blank=True, related_name='following')
    friends_list = models.ManyToManyField(User, blank=True, related_name='friends_list')


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    comment = models.TextField(max_length=2000, default="Enter Comment Here")
    created_on = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

class Post(models.Model):
    posts = models.TextField(max_length=1337, default="Enter post here")
    posts_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    date_and_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

