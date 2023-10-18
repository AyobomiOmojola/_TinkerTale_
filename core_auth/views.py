from rest_framework import status, permissions
from .serializers import RegisterSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import APIView 
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import User
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .serializers import UserProfileSerializer, FollowSerializer
from core_app.serializers import StoriesSerializer
from core_app.models import Userprofile, Stories, Follow




###############
######## REGISTER USERS:
###############

class RegisterView(APIView):
    serializer_class = RegisterSerializer

    @swagger_auto_schema(operation_summary="Register users", request_body=RegisterSerializer, tags=['Authentication'])

    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            user = serializer.save()


            response = {
                "MESSAGE": "User Created Successfully", 
                "REGISTERED_USER": serializer.data,
                #'token' : token.key
            }

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


###############
######## LOGIN USERS:
###############

class LoginView(APIView):

    @swagger_auto_schema(operation_summary="Login users", request_body=AuthTokenSerializer, tags=['Authentication'])

    def post(self, request: Request):
        serializer = AuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username = username, password = password)
            token, created = Token.objects.get_or_create(user=user)

            response = {
                "MESSAGE": "Login Successfull", 
                "TOKEN": token.key
            }

            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid email or password"})

    @swagger_auto_schema(operation_summary="Check for authentication", tags=['Authentication'])

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)


#############
##### LOGOUT USERS:
#############

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_summary="Logout users", tags=['Authentication'])

    def delete(self, request, format=None):
        request.user.auth_token.delete()
        return Response({"MESSAGE": "You are logged out"}, status=status.HTTP_200_OK)


#########
#### USERPROFILE:
#########

class CreateUserProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]

    ##### CREATE USERPROFILE:
    @swagger_auto_schema(operation_summary="Create your userprofile", request_body=UserProfileSerializer, tags=['Userprofile'])

    def post(self, request:Request):
        data = request.data

        serializer = UserProfileSerializer(data=data)

        if serializer.is_valid():

            serializer.save(user=self.request.user)

            response = {
                "MESSAGE":"UserProfile Created",
                "USERPROFILE":serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    ##### RETRIEVE YOUR USERPROFILE:
    @swagger_auto_schema(operation_summary="Retrieve your userprofile",operation_description="THIS ENDPOINT DISPLAYS YOUR USERPROFILE ALONG WITH THE STORIES YOU HAVE WRITTEN AND LIKED.", tags=['Userprofile'])

    def get(self, request:Request):
        userprofile = Userprofile.objects.filter(user = request.user)
        
        if userprofile:
            userprofile = Userprofile.objects.get(user = request.user)
            user_serializer = UserProfileSerializer(instance=userprofile)


            ### DISPLAY STORIES WRITTEN BY YOU:
            story = Stories.objects.filter(author = request.user)
            story_serializer = StoriesSerializer(instance=story, many=True)


            ##### DISPLAY STORIES LIKED BY YOU:
            liked_stories = Stories.objects.filter(liked_post__liker = request.user)
            likedstory_serializer = StoriesSerializer(instance=liked_stories, many=True)


            response = {
                    "MESSAGE":"Your Userprofile",
                    "PROFILE_DATA":user_serializer.data,
                    "STORIES_BY_USER":story_serializer.data,
                    "STORIES_LIKED_BY_USER":likedstory_serializer.data
                }

            return Response(data=response, status=status.HTTP_200_OK)
        
        else:
            return Response({'Message': 'No Userprofile Created!'}, status = status.HTTP_400_BAD_REQUEST)
    

    ##### UPDATE YOUR USER PROFILE:
    @swagger_auto_schema(operation_summary="Update your userprofile", request_body=UserProfileSerializer, tags=['Userprofile'])

    def put(self, request:Request):
        userprofile = Userprofile.objects.get(user = request.user)
        data = request.data
        serializer = UserProfileSerializer(instance=userprofile, data=data)

        if serializer.is_valid():

            serializer.save(user=self.request.user)

            response = {
                "MESSAGE":"UserProfile Updated!!!",
                "USERPROFILE":serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)




###############
###### VIEW OTHER PEOPLES PROFILE:
###############

class OtherUserProfile(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @swagger_auto_schema(operation_summary="View other userprofiles",operation_description="THIS ENDPOINT DISPLAYS OTHER USERPROFILES PAGE ALONG WITH THE STORIES THEY HAVE WRITTEN AND LIKED.", tags=['Userprofile'])

    def get(self, request:Request, username):
        userr = User.objects.get(username=username)
        userprofiles = Userprofile.objects.filter(user=userr)

        if userprofiles:
            userprofiles = Userprofile.objects.get(user=userr)
            user_serializer = UserProfileSerializer(instance=userprofiles)


            #### DISPLAY STORIES WRITTEN BY USER:
            story = Stories.objects.filter(author = userr)
            print(story)
            story_serializer = StoriesSerializer(instance=story,many=True)


            ##### STORIES LIKED BY USER
            liked_stories = Stories.objects.filter(liked_post__liker = userr)
            print(liked_stories)
            likedstory_serializer = StoriesSerializer(instance=liked_stories, many=True)

            response = {
                    "MESSAGE":"UserProfile of other user",
                    "PROFILE_DATA":user_serializer.data,
                    "STORIES_BY_USER":story_serializer.data,
                    "STORIES_LIKED_BY_USER":likedstory_serializer.data
                }

            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response({'Message': 'User has no Userprofile!'}, status = status.HTTP_400_BAD_REQUEST)


############
#### FOLLOW LOGIC FOR USERPROFILES:
############

class FollowLogic(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_summary="Follow users", tags=['Following/Followers'])

    def get(self, request:Request, username):
        followed = User.objects.get(username=username)
        follower = request.user
        already_followed = Follow.objects.filter(requestt_user=follower,other_user=followed)
        
        if not already_followed:
            follow = Follow(requestt_user=follower,other_user=followed)
            follow.save()
            serializer = FollowSerializer(instance=follow)

            response = {
                "MESSAGE":"You Successfully followed this user!!!",
                "FOLLOW":serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)


############
##### UNFOLLOW LOGIC FOR USERPROFILES:
############

class UnfollowLogic(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_summary="Unfollow users", tags=['Following/Followers'])

    def delete(self, request:Request, username):
        followed = User.objects.get(username=username)
        follower = request.user
        already_followed = Follow.objects.filter(requestt_user=follower,other_user=followed)
        already_followed.delete()

        return Response({"MESSAGE": "You just unfollowed this user"},status=status.HTTP_200_OK)


############
###### LIST OF FOLLOWERS IN RESPECTIVE USERPROFILES
###########

class ListOfFollowers(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_summary="Get list of followers", operation_description="YOUR FOLLOWERS MUST HAVE A USERPROFILE!", tags=['Following/Followers'])

    def get(self, request:Request):
        followers = Follow.objects.filter(other_user=request.user)
        list_of_followers = Userprofile.objects.filter(user__in=followers.values_list('requestt_user'))
        serializer = UserProfileSerializer(instance=list_of_followers, many=True)

        response = {
                "MESSAGE":"This is the list of your followers!!!",
                "FOLLOWERS":serializer.data
            }

        return Response(data=response, status=status.HTTP_200_OK)


###########
#### LIST OF FOLLOWED USERS IN RESPECTIVE USERPROFILES
###########

class ListofFollowing(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_summary="Get list of users you follow", operation_description="THE PEOPLE YOU FOLLOW MUST HAVE A USERPROFILE!", tags=['Following/Followers'])

    def get(self, request:Request):
        followers = Follow.objects.filter(requestt_user=request.user)
        list_of_followers = Userprofile.objects.filter(user__in=followers.values_list('other_user'))
        serializer = UserProfileSerializer(instance=list_of_followers, many=True)

        response = {
                "MESSAGE":"This is the list of people you follow!!!",
                "USERS_YOU_FOLLOW":serializer.data
            }

        return Response(data=response, status=status.HTTP_200_OK)