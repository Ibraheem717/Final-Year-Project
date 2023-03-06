from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


    
class MyUser(AbstractUser):
    date_of_birth = models.DateField( default='1970-01-01' )
    recommended = models.BooleanField(default=True)
    private = models.BooleanField(default=False)

    def getDOB(self):
        return self.date_of_birth
    
    def to_dict(self):
        return {
            'id' : self.id,
            'username': self.username,
            'password' : self.password,
            'email' : self.email,
            'dateOfBirth' : self.date_of_birth,
            'recommend' : self.recommended,
            'private' : self.private
        }
    
    def profile_info(self):
        return {
            'username': self.username,
            'email' : self.email,
            'date_of_birth' : self.date_of_birth,
        }
    
    def foreign_dict(self):
        if not self.private:
            return {
                "name" : self.username,
                "email" : self.email,
                "dateofbirth" : self.date_of_birth
            }

class Friends(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="User")
    friend = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="Friend")

    def to_dict(self):
        return {
            'user' : self.user.to_dict(),
            'friend' : self.friend.to_dict()
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
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=True, null=True)
    message = models.CharField(max_length=500)
    type = models.CharField(max_length=24)

    def GetMessage(self):
        return {
            'UserID' : self.user.to_dict(),
            'Message' : self.message
        }

class Forum (models.Model):
    creator = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=24, unique=True)

    def NumberOfUniqueUsers(self):
        length = []
        for i in ForumMessages.objects.filter( forum = self):
            length.append( i.message.user )
        return len(list(set(length)))

    def NumberOfMessages(self):
        length = 0
        for i in ForumMessages.objects.all():

            if (i.forum == self):
                print("hello")
            if i.forum.id == self.id:
                length += 1
        return length

    def to_dict(self):
        return {
            "id" : self.id,
            "Name" : self.name,
            "NumberOfMessages" : self.NumberOfMessages(),
            "NumberOfUsers" : self.NumberOfUniqueUsers(),
        }



class ForumTab (models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    name = models.CharField(max_length=54)

    def to_dict(self):
        return {
            'id' : self.id,
            'forum' : self.forum.to_dict(),
            'name' : self.name
        }

class Book (models.Model):
    id = models.CharField(max_length=13 , primary_key=True)
    name = models.CharField(max_length=24)
    pages = models.IntegerField(default=0)

    def GetISBN(self):
        return self.id

    def to_dict(self):
        return {
            'id' : self.id,
            'name' : self.name
        } 

class BookTracker (models.Model):
    class Meta:
        unique_together = (('book', 'user'),)

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    completed = models.BooleanField()
    read = models.IntegerField()

    def to_dict(self):
        return {
            'id' : self.id,
            'book' : self.book.to_dict(),
            'user' : self.user.to_dict(),
            'completed' : self.completed,
            'read' : self.read
        }

class BookTab (models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    name = models.CharField(max_length=54)

    def to_dict(self):
        return {
            'id' : self.id,
            'forum' : self.book.to_dict(),
            'name' : self.name
        }

class Author (models.Model):
    name = models.CharField(max_length=24)

    def to_dict(self):
        return {
            'id' : self.id,
            'name' : self.name
        }

class AuthorTab (models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    name = models.CharField(max_length=54)

    def to_dict(self):
        return {
            'id' : self.id,
            'forum' : self.author.to_dict(),
            'name' : self.name
        }
    
class ForumMessages(models.Model):
    message = models.ForeignKey(Messages, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)   
    tab = models.ForeignKey(ForumTab, on_delete=models.CASCADE, blank=True, null=True)     

    def to_dict(self):
        return {
            'message' : self.message.GetMessage(),
            'forum' : self.forum.to_dict(),
            'tab' : self.tab.to_dict()
        }

class BookMessages(models.Model):
    message = models.ForeignKey(Messages, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    tab = models.ForeignKey(BookTab, on_delete=models.CASCADE, blank=True, null=True)

    def to_dict(self):
        return {
            'message' : self.message,
            'book' : self.book
        }

class AuthorMessages(models.Model):
    message = models.ForeignKey(Messages, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tab = models.ForeignKey(AuthorTab, on_delete=models.CASCADE, blank=True, null=True)

    def to_dict(self):
        return {
            'message' : self.message,
            'author' : self.author
        }


class BookReviews(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.CharField(max_length=450)  

    def GetBook(self):
        return self.book 

    def to_dict(self):
        return {
            'user' : self.user.profile_info(),
            'book' : self.book.to_dict(),
            'rating' : self.rating,
            'review' : self.review
        }