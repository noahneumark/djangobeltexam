from __future__ import unicode_literals
import bcrypt
from django.db import models
from datetime import datetime

class UserManager(models.Manager):
    def regvalidation(self, postData):
        errors = []
        if len(postData['name']) < 3:
            errors.append("Name must be greater than 1 character.")
        if (postData['name'].replace(' ','').isalpha() == False):
            errors.append("First name must only be letters.")
        if len(postData['username']) < 3:
            errors.append("Username must be greater than 1 character.")
        if Users.objects.filter(username=postData['username']):
            errors.append("Username already taken.")
        if len(postData['password']) < 8:
            errors.append("Password must be at least 7 characters.")
        elif postData['password'] != postData['confpass']:
            errors.append("Password does not match password confirmation.")
        return errors
    def loginvalidation(self, postData):
        errors = []
        loginuser = Users.objects.filter(username=postData['username'])
        if loginuser:
            passtest = loginuser[0].password.encode()
        if not loginuser or bcrypt.hashpw(postData['password'].encode(), passtest) != passtest:
            errors.append("Invalid login")
        return errors
    def tripvalidation(self, postData):
        errors = []
        if len(postData['destination']) < 1:
            errors.append("Enter a destination")
        if len(postData['plan']) < 1:
            errors.append("Enter a trip plan")
        if len(postData['startdate']) < 1:
            errors.append("Enter a start date")
        elif datetime.strptime((postData['startdate']), '%Y-%m-%d') < datetime.now():
            errors.append("Start date must be in the future!")
        if len(postData['enddate']) < 1:
            errors.append("Enter an end date")
        elif datetime.strptime((postData['enddate']), '%Y-%m-%d') < datetime.strptime((postData['startdate']), '%Y-%m-%d'):
            errors.append("End date must be after the start date!")
        return errors


class Users(models.Model):
    name = models.CharField(max_length=80)
    username = models.CharField(max_length=80)
    password = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trips(models.Model):
    destination = models.CharField(max_length=80)
    plan = models.TextField()
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tripplanner = models.ForeignKey(Users, related_name="userplanner")
    usertrip = models.ManyToManyField(Users, related_name="travelbud")
