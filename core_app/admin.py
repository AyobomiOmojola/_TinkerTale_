from django.contrib import admin
from .models import *

admin.site.register(Genre)
admin.site.register(Stories)
admin.site.register(Like)
admin.site.register(Comment)
# admin.site.register(StoryImages)

class USerProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('age',)

class FollowAdmin(admin.ModelAdmin):
    list_display = ["requestt_user", "other_user"]



admin.site.register(Follow, FollowAdmin)

admin.site.register(Userprofile, USerProfileAdmin)




