from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, authenticate, login
from .forms import LoginForm, SignUpForm
from .models import MyUser, Forum, Book, Author, AuthorMessages, BookMessages, ForumMessages, Messages, UserGenres, BookReviews, BookTracker, ForumTab, Friends
from django.contrib import messages
from django.contrib.auth import logout
from PIL import Image
import numpy as np
import json, datetime, statistics, jwt
from re import IGNORECASE
from random import randint, shuffle
from math import ceil
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

file = pd.read_csv('mainapp\KaggleGoodReadsTest.csv')
cv = CountVectorizer(stop_words='english')
vectors = cv.fit_transform(file['genre'].apply(lambda x: np.str_(x))).toarray()
similarity = cosine_similarity(vectors)
RecommendedBooks = []
increment = 0

def index(request: HttpRequest):
    if request.method =='POST':
        form = LoginForm(request.POST, request.FILES)
        user = authenticate(username=form['username'].data, password=form['password'].data)
        if user:
            login(request, user)
            payload = {
                'id' : user.id,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat' : datetime.datetime.utcnow()
            } 

            # token  = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

            # reponse = Response()

            # response.set_cookie(key='jwt', value=token, httponly=True)
            # reponse.data = {
            #     'jwt' : token
            # }

            return HttpResponseRedirect("http://localhost:5173/Search")

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
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your account has been created')
        else:
            Wrong = True
            messages.error(request,'Invalid sign up details')

    form = SignUpForm()
    return render( request, "mainapp/signup.html" , { 
        'form' : form,
        'Wrong' : Wrong,
        } )


def get_user(request: HttpRequest) -> JsonResponse:
    if request.method=='GET':
        return JsonResponse ( {
            'user_id' : request.session.__getitem__("_auth_user_id")
        }, safe=False)

@csrf_exempt
def profile_api(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        data = json.loads(request.session.__getitem__("_auth_user_id"))
        user = MyUser.objects.get(id=data)
        # temp = user.getProfilePicture()
        # user_picture = Image.open(user.getProfilePicture(), mode='r')
        return JsonResponse ({
            'myUser' : [
                user.to_dict()
            ]
        })
    if request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        client = MyUser.objects.get(id=data['user_id'])
        included = False
        if data['field'] == 'username':
            client.username = data['change']
        elif data['field'] == 'email':
            client.email = data['change']
        elif data['field'] == 'password':
            client.password = data['change']
        elif data['field'] == 'date_of_birth':
            client.date_of_birth = data['change']
        elif data['field'] == 'recommend':
            client.recommended = data['change']
        elif data['field'] == 'private':
            client.private = data['change']
        client.save()
        return JsonResponse ({
            'myUser': [data],
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
        return JsonResponse ({
            'friend' : [i.to_dict() for i in Friends.objects.filter(user = MyUser.objects.get(id = user_id))]
        })


def Search(request:HttpRequest):
    bruh = []
    counter = []
    for i in range (20):
        number = randint(0, len(file))
        while number in counter:
            number = randint(0,len(file))
        bruh.append(file.iloc[number].to_json())
    return JsonResponse({"file" : bruh} , safe=False)

def SearchUser(request:HttpRequest, user_id:int):
    if request.method == "GET":
        user = MyUser.objects.get(id = user_id)
        user_books = []
        kaggle_books  = []
        for i in BookTracker.objects.filter(user = user):
            user_books.append(i.book.id)
        for i in user_books:
            kaggle_books.append((file[file['isbn'] == i]).to_json())
        temp = {}
        for i in BookTracker.objects.filter(user = user):
            temp.update( { i.book.id : i.to_dict() } )
        return JsonResponse({
            "UserBooks" : temp,
            "KaggleBooks" : kaggle_books,
            })

def SearchGeneral(request:HttpRequest, search:str):
    if request.method == "GET":
        temp_df = file[file['title'].str.contains(np.str_(search), flags=IGNORECASE)]
        temp = []
        for i in range (len(temp_df)):
            print(i)
            temp.append(temp_df.iloc[i].to_json())
        return JsonResponse({'file' : temp})

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

def getMessage( request: HttpRequest, medium: str , inputid : int):
    if request.method == "GET":
        
        existing = False
        item = None
        return_value = []

        if ( medium == 'Book' ):

            item = BookMessages.objects.filter( book =  inputid)

        elif ( medium == 'Forum' ):

            item = ForumMessages.objects.filter( forum = int(inputid) )
            item = ForumTab.objects.filter(forum = item)

        elif ( medium == 'Author' ):
            
            try:
                author = Author.objects.get(name=inputid)
            except Author.DoesNotExist:
                author = False
            if (author):
                item = AuthorMessages.objects.filter( author = int(author) )

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

        UserGenre = []

        CurrentUser = MyUser.objects.get(id = data['UserID'])

        try:
            CurrentBook = Book.objects.get(id = data['BookID'])
        except Book.DoesNotExist:
            CurrentBook = Book.objects.create(
                id = data['BookID'],
                name = data['BookName'],
                pages = data['total_pages']
            )
            CurrentBook.save()
        print(CurrentBook)

        try:
            AlreadyReview = BookReviews.objects.get(book = CurrentBook, user = CurrentUser)
        except BookReviews.DoesNotExist:
            BookReviews.objects.create(
                user = CurrentUser,
                book = CurrentBook,
                rating = data['Ratings'],
                review = data['Review']
            ).save()
            AlreadyReview = False

            
        print("This is herer : " , file[file['title'].str.contains(data['BookName'])])
        data['Genres'] = data['Genres'].split(',')
        print(data['Genres'])


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
        message_instance = Messages.objects.create(
            user = MyUser.objects.get( id = request.session.__getitem__("_auth_user_id")),
            message = data['msg'],
            type = medium
        )
        message_instance.save()

        if ( medium == "Book" ):

            if not (Book.objects.filter( id = data['BookID'])) :
                book = Book.objects.create(
                    id = data['BookID'],
                    name = data['BookName'],
                    pages = data['total_pages']
                )
                book.save()
            else:
                book = Book.objects.get( id = data['BookID'] )

            bookmessage_instance = BookMessages.objects.create(
                message = message_instance,
                book = book
            )
            bookmessage_instance.save()

        elif ( medium == "Forum" ):

            forum = Forum.objects.get( id = data['ForumID'] )

            ForumMessages.objects.create(
                message = message_instance,
                forum = forum,
                tab = ForumTab.objects.get( forum = forum , name = data['tab'])
            ).save()

        elif ( medium == "Author" ):

            try:
                AuthExist = Author.objects.get( name = data['AuthorID'] )
            except Author.DoesNotExist:
                AuthExist = False

            if not ( AuthExist ) :
                auth = Author.objects.create(
                    name = data['AuthorID']
                )
                auth.save()
            else:
                auth = Author.objects.get( name = data['AuthorID'] )

            AuthorMessages.objects.create(
                message = message_instance,
                author = auth
            ).save()
        
        return JsonResponse( { 'Passed' : True } )

def GetForums(request : HttpRequest):
    if request.method == 'GET':
        return JsonResponse( {
            "Forums" : [i.to_dict() for i in Forum.objects.all()]
        } )


def GetTabs(request : HttpRequest, forum_id):
    if request.method == 'GET':
        return JsonResponse( {
            "Forums" : [i.to_dict() for i in ForumTab.objects.filter( forum = Forum.objects.get(id = forum_id))]
        } )



def GetForumTabs(request : HttpRequest , forum_id, tab_name):
    if request.method == 'GET':
        return JsonResponse( {
            "Forums" : [i.to_dict() for i in ForumMessages.objects.filter( tab = ForumTab.objects.get( forum = Forum.objects.get(id = forum_id) , name = tab_name) )]
        } )

def GetTabUsers(request : HttpRequest, forum_id):
    if (request.method == 'GET'):
        messages = ForumMessages.objects.filter(tab = forum_id)
        users = []
        for i in messages:
            if i.message.user.id not in users:
                users.append(i.message.user.id)
        return JsonResponse ({
            'tab' : [MyUser.objects.get(id = i).to_dict() for i in users]
        })

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

@csrf_exempt
def CreateForumTab(request : HttpRequest):
    if request.method == "POST":
        data  = json.loads( request.body.decode('utf-8') )
        
        tab_forum = Forum.objects.get(id = data['forum'])

        try:
            if (ForumTab.objects.get(forum = tab_forum, name = data['name'])):
                return JsonResponse( { "Posted" : False } )
        except ForumTab.DoesNotExist:
            ForumTab.objects.create( forum = tab_forum, name = data['name'] ).save()



        return JsonResponse( { "Posted" : True } )

def GetRecommended(request: HttpRequest, start : int):
    if request.method == "GET":

        UserBooks = BookReviews.objects.filter(user = MyUser.objects.get(id = request.session.__getitem__("_auth_user_id")))

        if not (UserBooks):
            return JsonResponse({"Found" : False})

        MeanRating = sum([i.rating for i in UserBooks])/len(UserBooks) 
        print("I think this works : " , MeanRating)
        print(UserBooks)
        #sd = statistics.stdev([i.rating for i in UserBooks])

        AllBooks = []
        for i in UserBooks:
            if (i.rating >= MeanRating):
                AllBooks.append(i.book.name)

        print(AllBooks)

        ISBN = [str(i.GetBook().GetISBN()) for i in UserBooks]
        print ("\n", ISBN , "\n")


        ## Check if the input is lower
        ## Make reocmmended books global

        begin = 0
        upper = ceil(10/len(ISBN))

        while len(RecommendedBooks) < start+10:
            
            begin += int(upper*(start/10))
            print(len(RecommendedBooks), begin, upper)
            for i in ISBN:
                movie = file[file['isbn'] == i]
                if len(movie):
                    MovieIndex = movie.index[0]
                    distance = similarity[MovieIndex]
                    if (begin < len(distance)):
                        movie_list = sorted(enumerate(distance), reverse=True, key=lambda x : x[1])[begin:begin+upper]
                    for code in movie_list:
                        if (file.iloc[code[0]].isbn not in ISBN):
                            if (file.iloc[code[0]].isbn not in RecommendedBooks):
                                if (type(file.iloc[code[0]].isbn) == str):
                                    RecommendedBooks.append(file.iloc[code[0]].isbn)
            begin += upper


        # for i in ISBN:
        #     movie = file[file['isbn'] == i]
        #     if len(movie):
        #         print (movie.index)
        #         movie_index = movie.index[0]
        #         distance = similarity[movie_index]
        #         movie_list = sorted(enumerate(distance), reverse=True, key=lambda x : x[1])[:start+10]
        #         for code in movie_list:
        #             if (file.iloc[code[0]].isbn not in ISBN):
        #                 if (file.iloc[code[0]].isbn not in RecommendedBooks):
        #                     RecommendedBooks.append(file.iloc[code[0]].isbn)

        print (RecommendedBooks)

        # RecommendedBooks = RecommendedBooks[start:start+9]
        # for i in RecommendedBooks:
        #     if type(i) != str:
        #         RecommendedBooks.remove(i)

        # RecommendedBooks.append(file.iloc[ randint(0,len(file)) ].isbn)
        # shuffle(RecommendedBooks)

        return JsonResponse({"Found" : RecommendedBooks[start : start+10]})

def CheckCollection(request:HttpRequest, user_id:str, book_id:str):
    print("bob markley died")
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
            tracker = False


        return JsonResponse({'Tracker' : tracker.to_dict()})


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



def logout_view(request):
    logout(request)
    return redirect('./')
