from django.db import models

# Create your models here.

class Employer(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name

class Program(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name

class User(models.Model):
    last_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=50)
    last_contact = models.DateTimeField(blank=True, null=True)
    last_reply = models.DateTimeField(blank=True, null=True)
    last_program = models.ForeignKey('Program', blank=True, null=True)
    last_employer = models.ForeignKey('Employer', blank=True, null=True)
    last_role = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

class Survey(models.Model):
    user = models.ForeignKey('User', blank=False)
    date_sent = models.DateTimeField(blank=False)
    date_replied = models.DateTimeField(blank=True, null=True)
    external_id = models.CharField(max_length=200, unique=True, db_index=True)
    reply = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "%s - %s %s" % (self.external_id, self.user.first_name, self.user.last_name)
