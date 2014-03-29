from django.db import models

# Create your models here.

class Employer(models.Model):
    name = models.CharField(max_length=200)

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=50)
    last_contact = models.DateTimeField(blank=True)
    last_reply = models.DateTimeField(blank=True)
    last_employer = models.ForeignKey('Employer', blank=True, null=True)

class Survey(models.Model):
    user = models.ForeignKey('User', blank=False)
    date_sent = models.DateTimeField(blank=False)
    date_replied = models.DateTimeField(blank=True)
    external_id = models.CharField(max_length=200)
    reply = models.TextField(blank=True)
