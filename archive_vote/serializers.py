from rest_framework import serializers
from .models import  ReadLater, StoryForChallenge, StoryWriteUpChallenge, VoteForStories, EmeraldList


class ReadLaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadLater
        fields = ['owner','stories']


class StoryForChallengeSerializer(serializers.ModelSerializer):
    # images = ImageSerializer(many=True, read_only=True)
    
    # uploaded_images = serializers.ListField(
    #     child = serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False),
    #     write_only=True)
    class Meta:
        model = StoryForChallenge
        fields = ["author","genre", "title", "slug", "description","Story_content"]
        extra_kwargs = {
        "author" : {
            "read_only" : True,
        },
        "slug" : {
            "read_only" : True,
        }
    }



class BiWeeklyChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryWriteUpChallenge
        fields = ["story_line"]



class VoteForStoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteForStories
        fields = ["stories", "voter"]



class EmeraldListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmeraldList
        fields = ["stories"]