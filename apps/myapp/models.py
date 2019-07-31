from django.db import models
import re
import datetime
import bcrypt

from django.urls import reverse

# Create your models here.

# USER AUTHENTICATION
class UserManager(models.Manager):
    def reg_validator(self, form):
        errors = {}
        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+$")

        email = form['email']
        fname = form['fname']
        lname = form['lname']
        password = form['password']
        confirm = form['confirm']

        if not EMAIL_REGEX.match(email):
            errors['email'] = 'Invalid email address'
        else:
            users = User.objects.filter(email=email)
            if len(users) > 0:
                errors['email'] = 'Email address already exists'
        
        if len(password) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        elif confirm != password:
            errors['confirm'] = 'Passwords do not match!'
        
        return errors
    
    def login_validator(self, form):
        errors = {}
        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+$")

        email = form['email']
        password = form['password']

        users = User.objects.filter(email=email)
        
        if not EMAIL_REGEX.match(email):
            errors['email'] = 'Please enter a valid email address'
        elif len(users) < 1:
                errors['email'] = 'Please register'
        else:
            if not bcrypt.checkpw(password.encode(), User.objects.get(email = email).password.encode()):
                errors['email'] = "Incorrect password. Try again."

        return errors 
    
    def editvalidator(self, form):
        errors = {}
        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+$")

        email = form['email']
        fname = form['fname']
        lname = form['lname']

        users = User.objects.filter(email=email)
        if len(users) > 0:
            errors['email'] = 'Email address already exists'
        if not EMAIL_REGEX.match(email):
            errors['email'] = 'invalid'
        
        return errors
        

class MessageManager(models.Manager):
    def messageform(self, form):
        message = form['message']


class User(models.Model):
    email = models.CharField(max_length=255)
    fname = models.CharField(max_length=255, default="first")
    lname = models.CharField(max_length=255, default="last")
    password = models.CharField(max_length=255)
    description = models.TextField()
    user_level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Message(models.Model):
    body = models.CharField(max_length=255)
    author = models.ForeignKey(User, related_name='messagesposted', on_delete=models.CASCADE)
    profile = models.ForeignKey(User, related_name='profile', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MessageManager()

class Reply(models.Model):
    body = models.TextField()
    author = models.ForeignKey(User, related_name='replymessage', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='messagepost', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='replylikes')
    replies = models.ForeignKey(Message, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MessageManager()

