from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class MyUser(AbstractUser):
    date_of_birth = models.DateField( default='1970-01-01' )
    profile_picture = models.ImageField(upload_to='users/', default= 'defaultIcon.jpg')
    city = models.CharField(max_length=50, )

    def getDOB(self):
        return self.date_of_birth

    def getProfilePicture(self):
        return self.profile_picture.url

    
    def to_dict(self):
        return {
            'username': self.username,
            'password' : self.password,
            'email' : self.email,
            'dateOfBirth' : self.date_of_birth,
        }
    
    def profile_info(self):
        return {
            'username': self.username,
            'email' : self.email,
            'date_of_birth' : self.date_of_birth,
            'city' : self.city,
            'image' : self.profile_picture.url,
        }


class AuctionItem(models.Model):
    title = models.CharField( max_length=50 )
    description = models.CharField ( max_length=5000 )
    starting_price = models.DecimalField( max_digits=10, decimal_places=2 )
    current_price = models.DecimalField( max_digits=10, decimal_places=2 )
    item_picture = models.ImageField( upload_to='items/', default= 'defaultIcon.jpg')
    auction_finish = models.DateTimeField(  )
    item_owner = models.IntegerField(  )

    def to_dict(self):
        return {
            'ID' : self.id,
            'Title' : self.title,
            'Description' : self.description,
            'Starting Price' : self.starting_price,
            'Current Price' : self.current_price,
            'Item Picture' : self.item_picture.url,
            'Auction End' : self.auction_finish,
            'Owner' : self.item_owner
        }

class Question (models.Model) :
    question = models.CharField(max_length=500)
    user_id = models.IntegerField()
    item_id = models.IntegerField()
    answer = models.CharField(max_length=500)
    answered = models.BooleanField()

    def to_dict(self):
        return {
            'question_id' : self.id,
            'question_text' : self.question,
            'user_id' : self.user_id,
            'item_id' : self.item_id,
            'answer' : self.answer,
            'answered' : self.answered,
        }

class Answer (models.Model) :
    answer = models.CharField(max_length=500)
    item_id = models.IntegerField(  )
    question_id = models.IntegerField( )