from django.urls import path, re_path
from . import views

app_name = "core_auth"


urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("profile/", views.CreateUserProfile.as_view(), name="profile"),
    path("otherprofile/<username>/", views.OtherUserProfile.as_view(), name="other_profile"),
    # re_path(r'^otherprofile/(?P<username>.+)/$', views.OtherUserProfile.as_view(), name="other_profile"),
    path("follow/<username>/", views.FollowLogic.as_view(), name="follow"),
    path("unfollow/<username>/", views.UnfollowLogic.as_view(), name="unfollow"),
    path("followerslist/", views.ListOfFollowers.as_view(), name="followerslist"),
    path("followinglist/", views.ListofFollowing.as_view(), name="followinglist"),
]