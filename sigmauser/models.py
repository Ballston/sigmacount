from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    #Link UserProfile to User
    user=models.OneToOneField(User)
    description=models.CharField(db_column='description', max_length=512, blank=True, null=True)
    organisation=models.CharField(db_column='organisation', max_length=32, blank=True, null=True)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    
    #Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
    
    
class project(models.Model):
    projectid=models.AutoField(db_column='projectid',primary_key=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    projecttype=models.CharField(db_column='projecttype', max_length=32)
