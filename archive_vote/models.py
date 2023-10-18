from django.db import models
from django.contrib.auth.models import User
from core_app.models import Stories, Genre
import uuid

class StoryWriteUpChallenge(models.Model):
    story_line = models.TextField(verbose_name="Story line of the WriteUp")
    max_slots = models.IntegerField(blank=True, null=True)
    dead_line = models.DateField(blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)


class StoryForChallenge(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vote_story_author')
    genre = models.ManyToManyField(Genre, blank=False, related_name='genre_vote_stories')
    slug = models.SlugField(max_length=264, unique=True, default=uuid.uuid1)
    title = models.CharField(max_length=264, verbose_name="Put a Title")
    pub_date = models.DateTimeField(auto_now_add=True, )
    description =  models.TextField(verbose_name="Write a short descriptio of this story")
    Story_content = models.TextField(verbose_name="Tell your story...")

    def __str__(self):
        return f"{self.title}....... by ==> {self.author}"



class VoteForStories(models.Model):
    stories = models.OneToOneField(StoryForChallenge, on_delete=models.CASCADE, related_name='genre_vote_stories')
    voter = models.ManyToManyField(User, related_name='voterr')
    date_added = models.DateTimeField(auto_now_add=True, )

    def __str__(self):
        return '{}'.format(self.stories)


class EmeraldList(models.Model):
    stories = models.OneToOneField(StoryForChallenge, on_delete=models.CASCADE, related_name='emerald_stories')



class ReadLater(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_archive')
    stories = models.ManyToManyField(Stories, related_name="stories_archive")
    date_added = models.DateField(auto_now_add=True)