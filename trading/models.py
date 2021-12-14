from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, username,email,password):
        
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")
        
        user=self.model(
            email=self.normalize_email(email),
            username=username
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user 

    def create_superuser(self,email,username,password):
        user=self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
           
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user





class ideas(models.Model):
    user_name=models.CharField(max_length=255)
    trade_name=models.CharField(max_length=255)
    idea_name=models.CharField(max_length=255)
    trade_type=models.CharField(max_length=255)
    risk=models.CharField(max_length=255)
    target=models.CharField(max_length=255)
    stoploss=models.CharField(max_length=255)
    
    class Meta:
        db_table="ideas"



class event_list(models.Model):
    event_id=models.CharField(max_length=255,default=0)
    title=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    html_link=models.CharField(max_length=255)
    created_time=models.CharField(max_length=255)
    updated_time=models.CharField(max_length=255)
    start_time=models.CharField(max_length=255)
    end_time=models.CharField(max_length=255)
    attendee_name=models.CharField(max_length=255)
    attendee_email=models.CharField(max_length=255)
    creator=models.CharField(max_length=255)
    petsAllowed=models.BooleanField(default=True)
    formaldressCode=models.BooleanField(default=True)
    class Meta:
        db_table="event_list"


'''
class events(models.Model):
    event_id=models.CharField(max_length=255)
    title=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    html_link=models.CharField(max_length=255)
    created_time=models.DateTimeField(auto_now_add=True, blank=True)
    updated_time=models.DateTimeField(blank=True)
    start=models.CharField(max_length=255)
    end=models.CharField(max_length=255)
    attendees = models.JSONField()
    
    class Meta:
        db_table="event"

class new_events(models.Model):
    event_id=models.CharField(max_length=255)
    title=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    html_link=models.CharField(max_length=255)
    created_time=models.DateTimeField(auto_now_add=True, blank=True)
    updated_time=models.DateTimeField(blank=True)
    start=models.CharField(max_length=255)
    end=models.CharField(max_length=255)
    attendees = models.JSONField()
    
    class Meta:
        db_table="new_events"
'''


    
   