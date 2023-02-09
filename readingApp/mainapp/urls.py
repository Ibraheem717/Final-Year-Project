from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="Login"),
    path('sign-up', views.signup, name='SignUp'),

    path('ses-user', views.get_user, name="Get UserID"),
    path('user-image/<int:ID>', views.get_user_image, name="Get User's Image"),
    path('submit-user-image/<int:ID>', views.submit_user_image, name='Submit User Image'),
    path('user-profile', views.profile_api , name="View Profile"),

    path('Search', views.Search, name="Search"),
    path('SearchGeneral/<str:search>', views.SearchGeneral, name="Search General"),
    path('Search/<str:code>', views.SearchIndivisual, name="Search"),
    
    path('GetMessage/<str:medium>/<int:inputid>', views.getMessage, name=" Get Messages "),
    path('postReview', views.postReview, name=" Post a review "),
    path('postMessage/<str:medium>', views.postMessage, name=" Post a message "),

    path('GetForums', views.GetForums, name="All Forums"),
    path('CreateForum', views.CreateForum, name="Create Forum"),

    path('GetRecommendation/<int:start>', views.GetRecommended, name="Get recomended books"),

    path('logout', views.logout_view, name="Logout"),

    # path('all-items', views.all_item, name='All Items'),
    # path('my-all-items', views.my_all_item, name='All Items'),
    # path('submit-item-image/<int:ID>', views.submit_item_image, name='All Items'),
    
    # path('get-item/<int:ID>', views.get_item, name='All Items'),
    # path('submit-item/<int:ID>', views.submit_item, name='Submit Item'),
    # path('bid', views.up_bid, name='Up bid'),
    
    # path('search-items/<str:search_for>', views.Search , name="Search Items"),
    # path('get-questions/<int:item_id>', views.question_api),
    
    # path('questions', views.blog_api, name="Questions"),
]