from rest_framework import serializers, validators
from .models import Stories, Like, Comment, Genre


# class ImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StoryImages
#         fields = ["post", "image"]

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "genre"]
        extra_kwargs = {
        "id" : {
            "read_only" : True,
        },
        "genre" : {
            "read_only" : True,
        }
    }



class StoriesSerializer(serializers.ModelSerializer):
    # images = ImageSerializer(many=True, read_only=True)
    
    # uploaded_images = serializers.ListField(
    #     child = serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False),
    #     write_only=True)
    contentview = serializers.ChoiceField(choices=Stories.STORY_AGE_RATING)
    class Meta:
        model = Stories
        fields = ["author", "slug", "genre", "title", "description",  "storycontent", "contentview"]
        extra_kwargs = {
        "author" : {
            "read_only" : True,
        },
        "slug" : {
            "read_only" : True,
        }
    }
    
    # def create(self, validated_data):
    #     # uploaded_images = validated_data.pop("uploaded_images")
    #     genre = validated_data.pop('genre')
    #     story = Stories.objects.create(**validated_data)
    #     #for genres in genre:
    #     story.genre.set(genre)
    #     # for images in uploaded_images:
    #     #     newproduct_image = Images.objects.create(post=stories, image=images)
    #     return story


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['story','liker']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['story','user','comment']
        extra_kwargs = {
            'story':
            {
                "read_only" : True,
            },
            'user':
            {
                "read_only" : True,
            }
        }


