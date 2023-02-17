from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="Login"),
    path('sign-up', views.signup, name='SignUp'),
    path('ses-user', views.get_user, name="Get UserID"),
    path('user-profile', views.profile_api , name="View Profile"),
    path('GetForeignUser/<int:user>', views.GetForeignUser, name="Get Foreign User"),
    path('GetFriend/<int:user>', views.GetFriend, name="Get Foreign User"),

    path('Search', views.Search, name="Search"),
    path('SearchUser/<int:user_id>', views.SearchUser, name="Search"),
    path('SearchGeneral/<str:search>', views.SearchGeneral, name="Search General"),
    path('Search/<str:code>', views.SearchIndivisual, name="Search"),
    
    path('GetMessage/<str:medium>/<str:inputid>', views.getMessage, name=" Get Messages "),
    path('GetReview/<str:BookISBN>', views.GetReview, name="Get Book Review"),
    path('postReview', views.postReview, name=" Post a review "),
    path('postMessage/<str:medium>', views.postMessage, name=" Post a message "),

    path('GetForums', views.GetForums, name="All Forums"),
    path('GetTabs/<int:forum_id>', views.GetTabs, name="Forums Tabs"),
    path('GetForumTab/<int:forum_id>/<str:tab_name>', views.GetForumTabs, name="Forums Tabs"),
    path('GetTabUsers/<int:forum_id>', views.GetTabUsers, name="Forums Tabs Users"),    
    path('CreateForum', views.CreateForum, name="Create Forum"),
    path('CreateForumTab', views.CreateForumTab, name="Create Forum Tab"),

    path('GetRecommendation/<int:start>', views.GetRecommended, name="Get recomended books"),

    path('CheckCollection/<str:user_id>/<str:book_id>', views.CheckCollection, name="Check collection"),
    path('AddToColection', views.AddToColection, name="Add to collection"),
    path('UpdateCollection', views.UpdateCollection, name="Update collection"),


    path('logout', views.logout_view, name="Logout"),

]