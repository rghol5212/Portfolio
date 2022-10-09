from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(max_length=500, default="what is your Email?")


class SantasList(models.Model):
    name = models.CharField(max_length=15)
    email = models.EmailField(max_length=30)
    