from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=240, blank=False, default='')
    last_name = models.CharField(max_length=240, blank=False, default='')
    email = models.CharField(max_length=240, blank=False, default='', unique=True)
    phone_number = models.CharField(max_length=240, blank=False, default='', unique=True)
    address = models.CharField(max_length=240, blank=False, default='')
    identity_code = models.CharField(max_length=240, blank=False, default='')
    photo = models.CharField(max_length=240, blank=False, default='')
    password = models.CharField(max_length=240, blank=False, default='')
    rating = models.FloatField(default=0)
    role = models.CharField(max_length=240, blank=False, default='')


class Ride(models.Model):
    client = models.IntegerField(default=0)
    driver = models.IntegerField(default=0)
    source = models.CharField(max_length=240, blank=False, default='')
    day = models.CharField(max_length=240, blank=False, default='')
    time = models.CharField(max_length=240, blank=False, default='')
    destination = models.CharField(max_length=240, blank=False, default='')
    status = models.CharField(max_length=240, blank=False, default='')
    destination_name = models.CharField(max_length=240, blank=False, default='')
    price = models.FloatField(default=0)
    distance = models.FloatField(default=0)
    rating = models.FloatField(default=0)


class Request(models.Model):
    driver = models.IntegerField(default=0)
    identity = models.CharField(max_length=240, blank=False, default='')
    licence = models.CharField(max_length=240, blank=False, default='')
    matriculation = models.CharField(max_length=240, blank=False, default='')
    type = models.CharField(max_length=240, blank=False, default='')
    status = models.CharField(max_length=240, blank=False, default='')
