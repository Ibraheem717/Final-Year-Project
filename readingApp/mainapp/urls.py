from django.urls import path

from . import views

urlpatterns = [

    path('add', views.addtodatabase),
    path('', views.index, name="Login"),
    path('sign-up', views.signup, name='SignUp'),
    path('ses-user', views.get_user, name="Get UserID"),
    path('user-profile', views.profile_api , name="View Profile"),
    path('GetForeignUser/<int:user>', views.GetForeignUser, name="Get Foreign User"),

    path('GetFriends/<int:user_id>', views.GetFriends, name="Get Foreign User"),
    path('AddFriends', views.AddFriends, name="Add Foreign User"),
    path('CheckFriends/<int:user_id>/<int:friend_id>', views.CheckFriends, name="Add Foreign User"),

    path('Search', views.Search, name="Search"),
    path('SearchUser/<int:user_id>', views.SearchUser, name="Search"),
    path('SearchUser/<int:user_id>/<int:condition>', views.SearchFilteredUser, name="Search"),
    path('SearchGeneral/<str:search>', views.SearchGeneral, name="Search General"),
    path('Search/<str:code>', views.SearchIndivisual, name="Search"),
    
    path('GetMessage/<str:medium>/<str:inputid>/<str:tab_name>', views.getMessage, name=" Get Messages "),
    path('GetReview/<str:BookISBN>', views.GetReview, name="Get Book Review"),
    path('postReview', views.postReview, name=" Post a review "),
    path('postMessage/<str:medium>', views.postMessage, name=" Post a message "),

    path('GetForums', views.GetForums, name="All Forums"),
    path('GetAllTabs/<str:medium>/<int:object_id>', views.GetAllTabs, name="Forums Tabs"),
    path('GetTab/<int:forum_id>/<str:tab_name>', views.GetTab, name="Forums Tabs"),
    path('GetTabUsers/<str:medium>/<int:tab_id>', views.GetTabUsers, name="Forums Tabs Users"),    
    path('CreateTab', views.CreateTab, name="Create Forum Tab"),

    path('CheckAuthor/<str:author_name>', views.CheckAuthor, name="Check Author"),
    path('AuthorBooks/<str:author_name>', views.AuthorBooks, name="Check Author Books"),
    path('CreateForum', views.CreateForum, name="Create Forum"),

    path('GetRecommendation/<int:start>', views.GetRecommended, name="Get recomended books"),

    path('CheckCollection/<str:user_id>/<str:book_id>', views.CheckCollection, name="Check collection"),
    path('AddToColection', views.AddToColection, name="Add to collection"),
    path('UpdateCollection', views.UpdateCollection, name="Update collection"),


    path('logout', views.logout_view, name="Logout"),

]