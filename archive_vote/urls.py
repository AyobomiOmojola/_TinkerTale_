from django.urls import path
from . import views

urlpatterns = [
    path("storyforchallenge/", views.StoryForChallengeLogic.as_view(), name="storyforchallenge"),
    path("addtoarchive/<slug:story_slug>", views.AddToArchive.as_view(), name="addtoarchive"),
    path("voteforstory/<slug:story_slug>", views.VoteForAStory.as_view(), name="voteforstory"),
    path("biweeklywinners/", views.EmeraldStoryWinner.as_view(), name="biweeklywinners"),
    path("archivedstories/", views.GetArchivedStories.as_view(), name="archivedstories"),
    path("storycontext/", views.CreateStoryChallenge.as_view(), name="storycontext"),
]

