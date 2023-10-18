from django.contrib import admin
from .models import *

class ReadLaterAdmin(admin.ModelAdmin):
    list_display = ["owner"]

admin.site.register(ReadLater, ReadLaterAdmin)
admin.site.register(StoryForChallenge)
admin.site.register(StoryWriteUpChallenge)
admin.site.register(EmeraldList)
admin.site.register(VoteForStories)
# admin.site.register(VoteStoriesImages)


