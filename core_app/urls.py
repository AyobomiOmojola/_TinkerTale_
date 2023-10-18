from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home"),
    path("storiesbygenre/<str:genre>/", views.StoriesByGenre.as_view(), name="storiesbygenre"),
    path("allgenres/", views.AllGenres.as_view(), name="allgenres"),
    path("writestories/", views.WriteStories.as_view(), name="Write_Stories"),
    path("<slug:story_slug>/", views.RetrieveUpdateStories.as_view(), name="stories_detail"),
    path("like/<slug:story_slug>", views.LikeLogic.as_view(), name="like_user"),
    path("unlike/<slug:story_slug>", views.UnlikeLogic.as_view(), name="unlike_user"),
]