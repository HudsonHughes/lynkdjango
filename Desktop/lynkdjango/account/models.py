# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from django.db import models
from django.utils.six import with_metaclass
from django.contrib.auth.models import (
    UserManager as BaseUserManager, AbstractBaseUser, Group
)
from django.db.models.signals import ( pre_save, post_save )
from django.dispatch import receiver
import datetime
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, first_name, middle_name, last_name, username, email, password, **extra_fields):
        user = super().create_user(username,email,password)
        user.first_name = first_name
        user.middle_name = middle_name
        user.last_name = last_name
        user.save()
        return user

    def create_super_user(self, first_name, middle_name, last_name, username, email, password, year=None, **extra_fields):
        user = super().create_superuser_user(username, email, password)
        if year != None:
	        self.year = year
        user.first_name = first_name
        user.middle_name = middle_name
        user.last_name = last_name
        user.save()
        return user

    def create_admin_user(self, first_name, middle_name, last_name, username, email, password, **extra_fields):
        user = self.create_super_user(first_name, middle_name, last_name, username, email, password)
        g = Group.objects.get(name='admin')
        g.user_set.add(user)
        user.groups.add(g)
        user.save()
        return user

    def create_counselor_user(self, first_name, middle_name, last_name, username, email, password, **extra_fields):
        user = self.create_user(first_name, middle_name, last_name, username, email, password)
        g = Group.objects.get(name='counselor')
        g.user_set.add(user)
        user.groups.add(g)
        user.save()
        return user

    def create_instructor_user(self, first_name, middle_name, last_name, username, email, password, **extra_fields):
        user = self.create_user(first_name, middle_name, last_name, username, email, password)
        g = Group.objects.get(name='instructor')
        g.user_set.add(user)
        user.groups.add(g)
        user.save()
        return user

    def create_student_user(self, first_name, middle_name, last_name, username, email, password, **extra_fields):
        user = self.create_user(first_name, middle_name, last_name, username, email, password)
        print(user)
        g = Group.objects.get(name='student')
        g.user_set.add(user)
        user.groups.add(g)
        user.save()
        return user


class AdminManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(groups__name__in=['admin'])


class InstructorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(groups__name__in=['instructor'])


class CounselorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(groups__name__in=['counselor'])


class StudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(groups__name__in=['student'])


class User(AbstractUser):
    name_regex = RegexValidator(regex=r'^[A-Z][a-z]*$',
                                 message="Name or title must begin with a capital letter.")
    first_name = models.CharField(validators=[name_regex], max_length=30, null=True, blank=True)
    middle_name = models.CharField(validators=[name_regex], max_length=30, null=True, blank=True, default="")
    last_name = models.CharField(validators=[name_regex], max_length=30, null=True, blank=True)
    full_name = models.CharField(max_length=96, null=True, blank=True)
    full_name_initial = models.CharField(max_length=96, null=True, blank=True)
    address = models.CharField(max_length=144, null=True, blank=True, default='742 Evergreen Terrace')
    date_of_birth = models.DateField(blank=True, default=datetime.date(1996, 8, 1))

    year = models.IntegerField(blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    home_phone = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    cell_phone = models.CharField(validators=[phone_regex], max_length=15, blank=True)

    avatar_thumbnail = ProcessedImageField(default= 'avatars/default.jpg',
                                           # upload_to='avatars',
                                           # processors=[ResizeToFill(100, 50)],
                                           # format='JPEG',
                                           # options={'quality': 60}
                                           )
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    objects = UserManager()
    admins = AdminManager()
    counselors = CounselorManager()
    instructors = InstructorManager()
    students = StudentManager()


