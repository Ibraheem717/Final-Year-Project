from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect, FileResponse
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, authenticate, login
from .forms import LoginForm, SignUpForm
from .models import *
from django.contrib import messages
from django.contrib.auth import logout
from PIL import Image
import numpy as np
import json, datetime, statistics
from re import IGNORECASE
from random import randint, shuffle
from math import ceil
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity 
from sklearn.feature_extraction.text import CountVectorizer
from django.middleware import csrf

file = pd.read_csv('mainapp/KaggleGoodReadsTest.csv')
#Vectorize English words into tokens for comparison
cv = CountVectorizer(stop_words='english')
#Converts all the genres into tokens 
vectors = cv.fit_transform(file['genre'].apply(lambda x: np.str_(x))).toarray()
#Compares the token together and checks their similarity, displays an out starting from their mmost similat to least 
similarity = cosine_similarity(vectors)
RecommendedBooks = []
increment = 0

# Authenticates user if user exists using django methods
def index(request: HttpRequest):
    if request.method =='POST':
        form = LoginForm(request.POST, request.FILES)
        user = authenticate(username=form['username'].data, password=form['password'].data)
        if user:
            login(request, user)

            # return HttpResponseRedirect("http://localhost:5173/")

            return render(request, "mainapp/user/index.html")

        else:
            messages.error(request,'username or password not correct')
            return redirect('./')

    
    else:
        form = LoginForm()
        return render(request, "mainapp/index.html",{
            'form' : form,
    })

def signup(request: HttpRequest) -> HttpResponse:

    Wrong = False

    if (request.method == 'POST'):
        #Takes data from 'Forms'  made by 'Forms.py'
        form = SignUpForm(request.POST)
        # Checki form is valid, then save else give message
        if form.is_valid():
            form.save()
            messages.success(request,'Your account has been created')
        else:
            Wrong = True
            messages.error(request,'Invalid sign up details')

    #Message output depending on validity
    form = SignUpForm()
    return render( request, "mainapp/signup.html" , { 
        'form' : form,
        'Wrong' : Wrong,
        } )


def get_user(request: HttpRequest) -> JsonResponse:
    if request.method=='GET':
        # Get Login user
        return JsonResponse ( {
            'user_id' : request.session.__getitem__("_auth_user_id")
        }, safe=False)

@csrf_exempt
def profile_api(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        # Gets current user logged
        data = json.loads(request.session.__getitem__("_auth_user_id"))
        user = MyUser.objects.get(id=data)
        return JsonResponse ({
            'myUser' : [
                user.to_dict()
            ]
        })
    if request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        # Fetch user
        client = MyUser.objects.get(id=data['user_id'])
        included = False
        # Change Username  
        if data['field'] == 'username':
            # Check if username already exist
            if (MyUser.objects.get(username = data['change'])):
                return JsonResponse({
                    "included" : False,
                    "msg" : "User exists"
                })
            client.username = data['change']
        # Change e-mail
        elif data['field'] == 'email':
            client.email = data['change']
        # Change password
        elif data['field'] == 'password':
            # Compares current and user inputted
            if check_password(data['old_pass'], client.password ):
                client.set_password(data['change'])
            else:
                return JsonResponse({
                    "included" : False,
                    "msg" : "Wrong Password"
                })
        # Chagne DOB
        elif data['field'] == 'date_of_birth':
            client.date_of_birth = data['change']
        # Change Recommendation
        elif data['field'] == 'recommended':
            client.recommended = data['change']
            if not client.recommended:
                # Delete info about user
                UserGenres.objects.filter(user = client).delete()
                BookReviews.objects.filter(user = client).delete()
        # Privitisation
        elif data['field'] == 'private':
            client.private = data['change']
        client.save()
        return JsonResponse ({
            'included': included,
        })


def GetForeignUser(request : HttpRequest, user):
    if request.method == "GET":
        return JsonResponse({
            'user' : MyUser.objects.get(id = user).foreign_dict(),
            'private' : MyUser.objects.get(id = user).private,
            'recommend' : MyUser.objects.get(id = user).recommended
        })

def GetFriends(request:HttpRequest, user_id):
    if request.method == "GET":
        print 
        return JsonResponse ({
            'friend' : [i.to_dict() for i in Friends.objects.filter(user = MyUser.objects.get(id = user_id))]
        })

@csrf_exempt
def AddFriends(request:HttpRequest):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        Friends.objects.create(
            user = MyUser.objects.get(id = data['user']),
            friend = MyUser.objects.get(id = data['friend']),
        ).save()

        return JsonResponse({ "Saved" : True })


def CheckFriends(request:HttpRequest, user_id, friend_id):
    if request.method == "GET":
        try:
            return JsonResponse({
                'followed' : Friends.objects.get( user = user_id, friend = friend_id).to_dict()
            })
        except Friends.DoesNotExist:
            return JsonResponse ({
            'followed' : False
        })      

# Returns 20 random books
def Search(request:HttpRequest):
    bruh = []
    counter = []
    for i in range (20):
        number = randint(0, len(file))
        while number in counter:
            number = randint(0,len(file))
        bruh.append(file.iloc[number].to_json())
    return JsonResponse({"file" : bruh} , safe=False)

# Get filtered books
def SearchUserFound(user, condition = None):
    user = MyUser.objects.get(id = user)
    user_books = {}
    kaggle_books  = []
    for i in BookTracker.objects.filter(user = user):
        user_books.update( { i.book.id : i.to_dict() } )
    if condition != None:
        copy = user_books.copy()
        for i in user_books:
            if (user_books[i]['completed'] == condition):
                del copy[i]
        user_books = copy
    for i in user_books:
        kaggle_books.append((file[file['isbn'] == i]).to_json())
    return user_books, kaggle_books

# Get all user books
def SearchUser(request:HttpRequest, user_id:int):
    if request.method == "GET":
        temp, kaggle_books = SearchUserFound(user_id)
        return JsonResponse({
            "UserBooks" : temp,
            "KaggleBooks" : kaggle_books,
            })

# Get read or completed books
def SearchFilteredUser(request:HttpRequest, user_id:int, condition:int):
    user_books, kaggle_books = SearchUserFound(user_id, bool(condition))
    return JsonResponse({
            "UserBooks" : user_books,
            "KaggleBooks" : kaggle_books,
            })

# Search for books 
def SearchGeneral(request:HttpRequest, search:str):
    if request.method == "GET":
        temp_df = file[file['title'].str.contains(np.str_(search), flags=IGNORECASE)]
        temp = []
        for i in range (len(temp_df)):
            temp.append(temp_df.iloc[i].to_json())
        return JsonResponse({'file' : temp})

#Grab single books
def SearchIndivisual(request:HttpRequest, code:str):
    return JsonResponse({'Book' : file.loc[file['isbn'] == np.str_(code)].to_json()})


def UnravelMessage( item ) :
    message_id = []
    for i in item:
        message_id.append(i.to_dict()['message'])

    return_value = []
    for i in message_id:
        return_value.append( i.GetMessage() )

    return return_value

# Get message if they exist
def getMessage( request: HttpRequest, medium: str , inputid : int, tab_name :str):
    if request.method == "GET":
        
        existing = False
        item = None
        return_value = []

        if ( medium == 'Book' ):

            try:
                book = Book.objects.get(id=inputid)
                try: 
                    tab = BookTab.objects.get( book = book , name = tab_name)
                except BookTab.DoesNotExist:
                    tab = False
            except Book.DoesNotExist:
                book = False

            if (book and tab):
                item = BookMessages.objects.filter( tab = tab )

        elif ( medium == 'Forum' ):

            item = ForumMessages.objects.filter( forum = int(inputid) )
            item = ForumTab.objects.filter(forum = item)

        elif ( medium == 'Author' ):
            
            try:
                auth = Author.objects.get(name=inputid)
                try: 
                    tab = AuthorTab.objects.get( author = auth , name = tab_name)
                except AuthorTab.DoesNotExist:
                    tab = False
            except Author.DoesNotExist:
                auth = False

            if (auth and tab):
                item = AuthorMessages.objects.filter( tab = tab )


        if (item):

            return_value = UnravelMessage(item)
            existing = True
        else:

            return_value = {'UserID' : -1, 'Message' : ''}
        
        return JsonResponse( { 
            'Existing' : existing,
            'Values' : return_value
         } )

def GetReview(request : HttpRequest, BookISBN : str) :
    if (request.method == 'GET'):
        # Get review if it exist
        try:
            found_book = Book.objects.get(id = BookISBN)
        except Book.DoesNotExist:
            return JsonResponse({'Review' : False})
        return JsonResponse({"Reviews" : 
            [i.to_dict() for i in BookReviews.objects.filter( book = found_book )]})

@csrf_exempt
def postReview(request: HttpRequest):
    if request.method == 'POST':
        data = json.loads( request.body.decode('utf-8') )

        CurrentUser = MyUser.objects.get(id = data['UserID'])

        # Create book if it doesnt exist
        try:
            CurrentBook = Book.objects.get(id = data['BookID'])
        except Book.DoesNotExist:
            CurrentBook = Book.objects.create(
                id = data['BookID'],
                name = data['BookName'],
                pages = data['total_pages']
            )
            CurrentBook.save()

        # Makes a review if the user hasnt already made a review
        try:
            AlreadyReview = BookReviews.objects.get(book = CurrentBook, user = CurrentUser)
            return JsonResponse({"View" : False})
        except BookReviews.DoesNotExist:
            BookReviews.objects.create(
                user = CurrentUser,
                book = CurrentBook,
                rating = data['Ratings'],
                review = data['Review']
            ).save()
            AlreadyReview = False
            
        data['Genres'] = data['Genres'].split(',')

        # Update or create user prefered genres
        for i in data['Genres']:
            try :
                FindGenre = UserGenres.objects.get(genre = i)
                FindGenre.rating = (FindGenre.rating + float(data['Ratings']))/2
            except UserGenres.DoesNotExist:
                UserGenres.objects.create(
                    user = CurrentUser,
                    genre = i,
                    rating = data['Ratings']
                ).save()

        return JsonResponse( {"View" : AlreadyReview} )

@csrf_exempt
def postMessage(request: HttpRequest, medium: str) -> JsonResponse:
    if request.method == 'POST':
        data = json.loads( request.body.decode('utf-8') )

        #Create message
        message_instance = Messages.objects.create(
            user = MyUser.objects.get( id = request.session.__getitem__("_auth_user_id")),
            message = data['msg'],
            type = medium
        )
        message_instance.save()

        if ( medium == "Book" ):
            # Create book if it doesnt exist
            if not (Book.objects.filter( id = data['BookID'])) :
                book = Book.objects.create(
                    id = data['BookID'],
                    name = data['BookName'],
                    pages = data['total_pages']
                )
                book.save()
            else:
                book = Book.objects.get( id = data['BookID'] )

            # Create tab if it doesnt exist
            try:
                book_tab = BookTab.objects.get( book = book, name = data['tab'] )
            except BookTab.DoesNotExist:
                book_tab = BookTab.objects.create(
                    book = book,
                    name = data['tab']
                )
                book_tab.save()   

            # Make book message
            bookmessage_instance = BookMessages.objects.create(
                message = message_instance,
                book = book,
                tab = book_tab
            )
            bookmessage_instance.save()

        # Make forum message
        elif ( medium == "Forum" ):

            forum = Forum.objects.get( id = data['ForumID'] )

            ForumMessages.objects.create(
                message = message_instance,
                forum = forum,
                tab = ForumTab.objects.get( forum = forum , name = data['tab'])
            ).save()

        # Make author message
        elif ( medium == "Author" ):

            # Create author if they don't exist
            try:
                auth = Author.objects.get( name = data['AuthorID'] )
            except Author.DoesNotExist:
                auth = Author.objects.create(
                    name = data['AuthorID']
                )
                auth.save()

            # Create tab if it doesnt exist
            try:
                auth_tab = AuthorTab.objects.get( author = auth, name = data['tab'] )
            except AuthorTab.DoesNotExist:
                auth_tab = AuthorTab.objects.create(
                    author = auth,
                    name = data['tab']
                )
                auth_tab.save()   


            AuthorMessages.objects.create(
                message = message_instance,
                author = auth,
                tab = auth_tab
            ).save()
        
        return JsonResponse( { 'Passed' : True } )

def GetForums(request : HttpRequest):
    if request.method == 'GET':
        return JsonResponse( {
            "Forums" : [i.to_dict() for i in Forum.objects.all()]
        } )


def GetAllTabs(request : HttpRequest, medium , object_id):
    if request.method == 'GET':
        if (medium == "Forum"):
            return JsonResponse( {
                "Forums" : [i.to_dict() for i in ForumTab.objects.filter( forum = Forum.objects.get(id = object_id))]
            } )
        elif (medium == "Author"):
            try:
                auth = Author.objects.get(id = object_id)
                return JsonResponse( {
                    "Author" : [i.to_dict() for i in AuthorTab.objects.filter( author = auth)]
                } )
            except Author.DoesNotExist:
                return JsonResponse({"Authour" : False})
        elif (medium == "Book"):
            try:
                book = Book.objects.get(id = object_id)
                return JsonResponse( {
                    "Book" : [i.to_dict() for i in BookTab.objects.filter( book = book)]
                } )
            except Book.DoesNotExist:
                return JsonResponse({"Book" : False})


# Poor programming
def GetTab(request : HttpRequest , forum_id, tab_name):
    if request.method == 'GET':
        return JsonResponse( {
            "Forums" : [i.to_dict() for i in ForumMessages.objects.filter( tab = ForumTab.objects.get( forum = Forum.objects.get(id = forum_id) , name = tab_name) )]
        } )

# Get users in tab
def GetTabUsers(request : HttpRequest, medium:str, tab_id):
    if (request.method == 'GET'):
        if medium == "forum":
            messages = ForumMessages.objects.filter(tab = tab_id)
        if medium == "author":
            messages = AuthorMessages.objects.filter(tab = tab_id)
        if medium == "book":
            messages = BookMessages.objects.filter(tab = tab_id)
        users = []
        for i in messages:
            if i.message.user.id not in users:
                users.append(i.message.user.id)
        return JsonResponse ({
            'tab' : [MyUser.objects.get(id = i).to_dict() for i in users]
        })

@csrf_exempt
def CreateTab(request : HttpRequest):
    if request.method == "POST":
        data  = json.loads( request.body.decode('utf-8') )
        
        

        if (data['medium'] == "forum"):
            tab_forum = Forum.objects.get(id = data['forum'])
            try:
                if (ForumTab.objects.get(forum = tab_forum, name = data['name'])):
                    return JsonResponse( { "Posted" : False } )
            except ForumTab.DoesNotExist:
                ForumTab.objects.create( forum = tab_forum, name = data['name'] ).save()

        elif (data['medium'] == "author"):
            author_forum = Author.objects.get(id = data['author'])
            try:
                if (AuthorTab.objects.get(author = author_forum, name = data['name'])):
                    return JsonResponse( { "Posted" : False } )
            except AuthorTab.DoesNotExist:
                AuthorTab.objects.create( author = author_forum, name = data['name'] ).save()

        elif (data['medium'] == "book"):
            book_forum = Book.objects.get(id = data['book'])
            try:
                if (BookTab.objects.get(book = book_forum, name = data['name'])):
                    return JsonResponse( { "Posted" : False } )
            except BookTab.DoesNotExist:
                BookTab.objects.create( book = book_forum, name = data['name'] ).save()


        return JsonResponse( { "Posted" : True } )

def CheckAuthor(request:HttpRequest, author_name):
    if request.method == "GET":
        try:
            return JsonResponse({'Author' : Author.objects.get(name = author_name).to_dict()})
        except Author.DoesNotExist:
            return JsonResponse({'Author' : False})

# Grab books written by author
def AuthorBooks(request:HttpRequest, author_name:str):
    if request.method == "GET":
        if author_name != "Unknown":
            return JsonResponse({
                'Books' : file.loc[file['author'].str.contains(author_name)].to_json()
            })
        return JsonResponse({'Books' : False})


@csrf_exempt
def CreateForum(request : HttpRequest):
    if request.method == "POST":
        data  = json.loads( request.body.decode('utf-8') )

        try:
            if (Forum.objects.get(name = data['Name'])):
                return JsonResponse( { "Posted" : False } )
        except Forum.DoesNotExist:
            new_forum = Forum.objects.create( creator = MyUser.objects.get(id = data['user']), name = data['Name'] )
            new_forum.save()
            ForumTab.objects.create( forum = new_forum, name = "main" ).save()


        return JsonResponse( { "Posted" : True } )


def GetRecommended(request: HttpRequest, start : int):
    if request.method == "GET":
        # Gets user
        myuser = MyUser.objects.get(id = request.session.__getitem__("_auth_user_id"))

        # Check if user allows recommendation
        if not myuser.recommended:
            return JsonResponse({'Found' : False})
 
        UserBooks = BookReviews.objects.filter(user = myuser)

        # Returns if user hasnt reviewed a book
        if not (UserBooks):
            return JsonResponse({"Found" : False})

        # Mean rating
        MeanRating = sum([i.rating for i in UserBooks])/len(UserBooks) 

        # Taking >Mean rating
        AllBooks = []
        for i in UserBooks:
            if (i.rating >= MeanRating and i.rating >= 3):
                AllBooks.append(i)

        # Store ISBN of books
        ISBN = [str(i.GetBook().GetISBN()) for i in AllBooks]
        ALLISBN = [str(i.GetBook().GetISBN()) for i in UserBooks]


        ## Check if the input is lower
        ## Make reocmmended books global
           
        for i in ISBN:
            # Finding and checking if ISBN exist
            book = file[file['isbn'] == i]
            if len(book):
                BookIndex = book.index[0]
                # Grapping all similarities from least to highest
                distance = similarity[BookIndex]
                if (len(distance)):
                    # Reversing from highest to least
                    book_list = sorted(enumerate(distance), reverse=True, key=lambda x : x[1])[:10]
                # Remvoing duplicates/books already existing
                for code in book_list:
                    if (file.iloc[code[0]].isbn not in ALLISBN):
                        if (file.iloc[code[0]].isbn not in RecommendedBooks):
                            if (type(file.iloc[code[0]].isbn) == str):
                                RecommendedBooks.append(file.iloc[code[0]].isbn)

        shuffle(RecommendedBooks)
        #Return books
        return JsonResponse({"Found" : RecommendedBooks})

# Checks if book is in collection
def CheckCollection(request:HttpRequest, user_id:str, book_id:str):
    if request.method == "GET":
        try:
            booked = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
             return JsonResponse({'Tracker' : False})
        try:
            tracker = BookTracker.objects.get(
                user = MyUser.objects.get(id=user_id),
                book = booked
            )
        except BookTracker.DoesNotExist:
            return JsonResponse({'Tracker' : False})



        return JsonResponse({'Tracker' : tracker.to_dict()})

# Adds book to collection
@csrf_exempt
def AddToColection(request:HttpRequest):
    if request.method == "POST":
        data = json.loads( request.body.decode('utf-8'))

        try :
            fetched_book = Book.objects.get(id = data['isbn'])
        except Book.DoesNotExist:
            fetched_book = Book.objects.create(
                id = data['isbn'],
                name = data['name'],
                pages = data['total_pages']
            )
            fetched_book.save()

        test = MyUser.objects.get(id = int(data['user_id']))

        bt = BookTracker.objects.create(
            book = fetched_book,
            user = MyUser.objects.get( id = data['user_id'] ),
            completed = data['completed'],
            read = data['read']
        )
        bt.save()

        print(bt.to_dict())

        return JsonResponse({'Tracker' : bt.to_dict()})
    
# Updates pages or completed status
@csrf_exempt
def UpdateCollection(request:HttpRequest):
    if request.method == "PUT":
        data = json.loads(  request.body.decode('utf-8') )
        book_selected  = Book.objects.get(id = data['book_id'])
        tracker = BookTracker.objects.get(book = book_selected, user = MyUser.objects.get(id = data['user_id']))
        if int(data['pages']) > tracker.read:
            if int(data['pages']) >= book_selected.pages:
                tracker.read = book_selected.pages
                tracker.completed = True
            else:
                tracker.read = data['pages']
            tracker.save()
            return JsonResponse({'Updated' : True})
        return JsonResponse({'Updated' : False})


def addtodatabase(request):
    for row in file.itertuples():
        print(row[1])

    for i in file:
        print (i)

    return JsonResponse({})


def logout_view(request):
    logout(request)
    return redirect('./')
