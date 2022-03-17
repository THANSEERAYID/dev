import email
from email.policy import default
from django.contrib.auth.models import AbstractUser
from cgitb import text
from pyexpat import model
from statistics import mode
from turtle import update
from django.db import models
from django.forms import NullBooleanField, TimeField
from django.contrib.auth.models import AbstractUser

from sqlalchemy import null, true




# Create your models here.

class User(AbstractUser):
    name=models.CharField(max_length=200, null=True)
    email=models.EmailField(unique=True, null=True)
    bio=models.TextField(null=True)

    avatar=models.ImageField(null=True, default="avatar.svg")
   
    REQUIRED_FIELD=[]

class Topic(models.Model):
    name=models.CharField(max_length=64)
    
    def __str__(self):
        return self.name

class Room(models.Model):
    topic=models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    host=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name=models.CharField(max_length= 64)
    description=models.TextField(null=True, blank=True)
    participants=models.ManyToManyField(User, related_name='participants', blank=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering =['-updated', '-created']

    def __str__(self):
        return self.name


class Messages(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    room=models.ForeignKey(Room, on_delete=models.CASCADE)
    body=models.TextField()

    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =['-updated', '-created']

    def __str__(self):
        return self.body





