from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import uuid


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=264, blank=False)

    def __str__(self):
        return f"{self.genre}"



class Stories(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_author')
    genre = models.ManyToManyField(Genre, blank=False, related_name='genre_stories')
    slug = models.SlugField(max_length=264, unique=True, default=uuid.uuid1)
    title = models.CharField(max_length=264, verbose_name="Put a Title")
    pub_date = models.DateTimeField(auto_now_add=True, )
    description =  models.TextField(verbose_name="Write a short description of this story")
    storycontent = models.TextField(verbose_name="Tell your story...")
    STORY_AGE_RATING = (
        ('G','General audience'),
        ('R','Restricted')
    )
    contentview = models.CharField(blank = False, choices=STORY_AGE_RATING, max_length = 10,)

    def __str__(self):
        return f"{self.title}({self.contentview})....... by ==> {self.author}"



class Like(models.Model):
    story = models.ForeignKey(Stories, on_delete=models.CASCADE, related_name='liked_post')
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liker')
    date_created = models.DateTimeField(auto_now_add=True)
# ManytoMany field could work but for the sake of referencing visa-vis i want each object instance to be unique.
    def __str__(self):
        return '{} ...liked the story>>>[{}]'.format(self.liker, self.story)


class Comment(models.Model):
    story = models.ForeignKey(Stories, on_delete=models.CASCADE, related_name='story_comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-comment_date']

    def __str__(self):
        return '{} commented on => {}'.format(self.user, self.story)


# class StoryImages(models.Model):
#     post = models.ForeignKey(Stories, on_delete=models.CASCADE, related_name = "images")
#     image = models.ImageField(upload_to='story_pic',verbose_name='Image')



class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user_profile')
    interested_genres = models.ManyToManyField(Genre, related_name='profile_genre')
    profile_pic = models.ImageField(upload_to='profile_pic', null=True, blank=True)
    bio = models.CharField(max_length=264, verbose_name="Write a short bio about yourself")
    date_of_birth = models.DateField(null = True)

    @property
    def age(self):
        return int((datetime.now().date() - self.date_of_birth).days / 365.25)
    
    def __str__(self):
        return '{}'.format(self.user)



class Follow(models.Model):
    requestt_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    other_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')