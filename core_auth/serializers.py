from django.contrib.auth.models import User
from rest_framework import serializers, validators
from core_app.models import Userprofile, Follow


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "password")
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), f"A user with that Email already exists."
                    )
                ],
            },
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user
    



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userprofile
        fields =  ['user','interested_genres','bio','date_of_birth','age']

        extra_kwargs = {
        "user" : {
            "read_only" : True,
        },
        "age": {
            "read_only" : True
        }
    }


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['requestt_user','other_user']

        extra_kwargs = {
            'requestt_user' : {
                "read_only" : True,
            },
            'other_user' : {
                "read_only" : True,
            }
        }

class ToFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userprofile
        fields =  ['user','bio','age']

    #     extra_kwargs = {
    #     "age": {
    #         "read_only" : True
    #     }
    # }