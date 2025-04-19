from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.email import send_account_activation_email
# Create your models here.

class College(models.Model):
    name = models.CharField(max_length=255, unique=True)
    established_year = models.IntegerField()
    rating = models.FloatField()
    average_fees = models.IntegerField()

    def __str__(self):
        return self.name
    

class Recommendation(models.Model):
    rank = models.IntegerField()
    percentile = models.FloatField()
    category = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    branch = models.CharField(max_length=100)  # Add this field for user input

    recommended_colleges = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Recommendation for Rank {self.rank}"
    
class Profile(BaseModel):
    user= models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    is_email_verified=models.BooleanField(default=False)
    email_token=models.CharField(max_length=100, null=True,blank=True)
    #profile_image=models.ImageField(upload_to="profile")
    
    def _str_(self):
        return f"{self.user.username}'s Profile"
@receiver(post_save, sender=User)
def send_email_token(sender, instance, created ,**kwargs):
    try:
        if created:
            email_token=str(uuid.uuid4())
            Profile.objects.create(user=instance ,email_token=email_token)
            email=instance.email
            send_account_activation_email(email,email_token)

    except Exception as e:
        print(e)