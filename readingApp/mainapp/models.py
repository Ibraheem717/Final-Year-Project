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

    def getInterest(self):
        return self.interest

    
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

class UserGenres(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=True, null=True)
    genre = models.CharField(max_length=24)
    rating = models.FloatField(max_length=2)

    def to_dict(self):
        return {
            "User" : self.user.to_dict(),
            "Genre" : self.genre,
            "Rating" : self.rating
        }

class Messages (models.Model):
    user_id = models.IntegerField()
    message = models.CharField(max_length=500)
    type = models.CharField(max_length=24)

    def GetMessage(self):
        return {
            'UserID' : self.user_id,
            'Message' : self.message
        }

class Forum (models.Model):
    name = models.CharField(max_length=24, unique=True)

    def NumberOfUniqueUsers(self):
        length = []
        for i in ForumMessages.objects.filter( forum_id = self):
            length.append( i.message_id.user_id )
        return len(list(set(length)))

    def NumberOfMessages(self):
        length = 0
        for i in ForumMessages.objects.all():

            if (i.forum_id == self):
                print("hello")
            if i.forum_id.id == self.id:
                length += 1
        return length

    def to_dict(self):
        return {
            "id" : self.id,
            "Name" : self.name,
            "NumberOfMessages" : self.NumberOfMessages(),
            "NumberOfUsers" : self.NumberOfUniqueUsers(),
        }

class Book (models.Model):
    id = models.IntegerField(max_length=13 , primary_key=True)
    name = models.CharField(max_length=24)

    def GetISBN(self):
        return self.id

class Author (models.Model):
    name = models.CharField(max_length=24)
    
class ForumMessages(models.Model):
    message_id = models.ForeignKey(Messages, on_delete=models.CASCADE)
    forum_id = models.ForeignKey(Forum, on_delete=models.CASCADE)        

    def to_dict(self):
        return {
            'message' : self.message_id,
            'forum_id' : self.forum_id
        }

class BookMessages(models.Model):
    message_id = models.ForeignKey(Messages, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)

    def to_dict(self):
        return {
            'message' : self.message_id,
            'book_id' : self.book_id
        }

class AuthorMessages(models.Model):
    message_id = models.ForeignKey(Messages, on_delete=models.CASCADE)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)

    def to_dict(self):
        return {
            'message' : self.message_id,
            'author_id' : self.author_id
        }


class BookReviews(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(max_length=1)
    review = models.CharField(max_length=450)  

    def GetBook(self):
        return self.book 