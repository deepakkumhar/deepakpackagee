from pyexpat import model
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractUser
import uuid


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    birth_date = models.DateField(null=True)

    is_verified = models.BooleanField(default=False)
    is_actives = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


    def __str__(self):
        return self.username

    

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class userPost(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    userImage= models.ImageField( upload_to='image/',default=None)
    caption=models.CharField(max_length=20,null=True)

# class userCommunication(models.Model):
#     user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
#     userPost=models.ForeignKey(userPost,on_delete=models.DO_NOTHING)
#     like=models.BooleanField(default=False)
#     comment=models.CharField(max_length=600,null=True)    




#for recursion

class postDetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    PostId=models.ForeignKey(userPost,on_delete=models.DO_NOTHING)
    likes=models.BooleanField(default=False)
    comments=models.CharField(max_length=800,null=True)
    parents=models.ForeignKey('self',null=True,blank=True,related_name='sub_comment',on_delete=models.DO_NOTHING,)
    views =models.IntegerField(null=True)

    







    