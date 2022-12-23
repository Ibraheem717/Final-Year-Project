from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, authenticate, login
from .forms import LoginForm, SignUpForm
from .models import MyUser, AuctionItem, Question
from django.contrib import messages
from django.contrib.auth import logout
from PIL import Image
import json, datetime

def index(request: HttpRequest):
    if request.method =='POST':
        form = LoginForm(request.POST, request.FILES)
        user = authenticate(username=form['username'].data, password=form['password'].data)
        if user:
            login(request, user)
            return HttpResponseRedirect("http://localhost:5173/view_items")

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



@csrf_exempt
def get_user(request: HttpRequest) -> JsonResponse:
    if request.method=='GET':
        return JsonResponse ( {
            'user_id' : request.session.__getitem__("_auth_user_id")
        }, safe=False)

def all_item(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        return JsonResponse (
            [i.to_dict() for i in AuctionItem.objects.all()]
         , safe=False)

def my_all_item(request: HttpRequest) -> JsonResponse:

    if request.method == 'GET':
        Items = [i.to_dict() for i in AuctionItem.objects.filter(item_owner=request.session.__getitem__("_auth_user_id"))]
        return JsonResponse (
           {'items' : [i for i in Items]}, safe=False
        )

@csrf_exempt
def submit_item_image(request: HttpRequest, ID : int) -> HttpResponseRedirect:
    print ("THis is ID: ", ID)
    if request.method == 'POST':
        data = request.FILES['my_image']
        print("Request Files: ", data)
        obj = AuctionItem.objects.get(id=ID)
        obj.item_picture = data
        obj.save()
        return HttpResponseRedirect("http://localhost:5173/my_items")

@csrf_exempt
def submit_user_image(request: HttpRequest, ID : int) -> HttpResponseRedirect:
    if request.method == 'POST':
        data = request.FILES['my_image']
        obj = MyUser.objects.get(id=ID)
        obj.profile_picture = data
        obj.save()
        return HttpResponseRedirect("http://localhost:5173/Profile")


def get_item(request: HttpRequest, ID : int) -> JsonResponse:
    if request.method == 'GET':
        item_selected = AuctionItem.objects.get(id = ID)
        return JsonResponse (
            {'return_item' : item_selected.to_dict()} ,safe=False
        )

def get_user_image(request: HttpRequest, ID : int):
    user = MyUser.objects.get(id=ID)
    user_profile = Image.open(user.getProfilePicture(), mode='r')
    return render(FileResponse(open(user.getProfilePicture(), 'rb')))


@csrf_exempt
def submit_item(request: HttpRequest, ID : int) -> HttpResponseRedirect:
    proceed  = True
    if request.method == 'POST':
        data = request.POST
        data_image = request.FILES['my_image']
        
        if ( datetime.datetime.strptime(data['auction_finish'], "%Y-%m-%dT%H:%M")< datetime.datetime.now()):
            proceed = False
        if proceed:
            client = AuctionItem(
                title = data['title'],
                description = data['description'],
                starting_price = data['starting_price'],
                current_price = data['starting_price'],
                auction_finish = data['auction_finish'],
                item_picture = data_image,
                item_owner = ID
            )
            client.save()
        return HttpResponseRedirect("http://localhost:5173/auctionForm")

@csrf_exempt
def up_bid(request : HttpRequest) -> JsonResponse:

    if request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        client = AuctionItem.objects.get(id=data['ID'])
        accepted = True
        if client.item_owner == data['item_owner']:
            accepted = False
        if client.current_price > data['new_bid']:
            accepted = False
        if (client.auction_finish < datetime.datetime.now() ):
            accepted = False
        if accepted:
            client.current_price = data['new_bid']
            client.save()
        return JsonResponse ({
            'success' : accepted
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
                user.profile_info()
            ]
        })
    if request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        client = MyUser.objects.get(id=data['user_id'])
        included = False
        if data['username'] != client.username:
            check_user = MyUser.objects.filter(username = data['username'])
            if len(check_user) != 0 :
                included = True
        if included == False:
            client.username = data['username']
            client.email = data['email']
            client.date_of_birth = data['date_of_birth']
            client.city = data['city']
            client.save()
        return JsonResponse ({
            'myUser': [data],
            'included': included,
        })

@csrf_exempt
def blog_api(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        item = AuctionItem.objects.get(id=data['item_id'])
        saved = False
        print(item.item_owner)
        print( data['user_id'])

        if ( int(item.item_owner) != int(data['user_id']) ):
            if (data['question'] != ""):
                client = Question.objects.create(
                    question = data['question'],
                    user_id = data['user_id'],
                    item_id = data['item_id'],
                    answer = "",
                    answered = False,
                )
                print("BOB JIONED THE ARNMY")
                saved = True
        print(saved)
        return JsonResponse({
            'question' : [saved]
        })
    if request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        client = Question.objects.get(id=data['question_id'])
        if (data['answer'] != ""):
            if client.answered == False:
                client.answer = data['answer']
                client.answered = True
                client.save()
        return JsonResponse({
            'question': [data],
        })

@csrf_exempt
def question_api(request: HttpRequest, item_id: int) -> JsonResponse:
    if request.method == 'GET':
        current_item = [question.to_dict() for question in Question.objects.filter(item_id=item_id)]
        return JsonResponse({
            'questions': [
                question for question in current_item
            ]
        }, safe = False)

def Search(request : HttpRequest, search_for : str) -> JsonResponse:
    if request.method == 'GET':
        items_title = AuctionItem.objects.filter( title__icontains=search_for )
        items_desc = AuctionItem.objects.filter( description__icontains=search_for )
        items = [i.to_dict() for i in items_title] + [i.to_dict() for i in items_desc]
        print(items)
        return JsonResponse({
            'responses' : items,
        })


def logout_view(request):
    logout(request)
    return redirect('./')

