from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Forum, Book, Author, AuthorMessages, BookMessages, ForumMessages, Messages, UserGenres, BookReviews

admin.site.register(MyUser, UserAdmin)
# Register your models here.

admin.site.register(UserGenres)

admin.site.register(Forum)

admin.site.register(ForumMessages)

admin.site.register(Book)

admin.site.register(BookMessages)

admin.site.register(Author)

admin.site.register(AuthorMessages)

admin.site.register(Messages)

admin.site.register(BookReviews)
