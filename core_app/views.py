from rest_framework.decorators import APIView 
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from .models import Userprofile, Stories, Like, Comment, Follow, Genre
from .serializers import StoriesSerializer, LikeSerializer, CommentSerializer, GenreSerializer
from core_auth.serializers import ToFollowSerializer
from django.db.models import Count




class HomeView(APIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="This serves data for the home page", operation_description="STORIES WRITTEN IN TINKERTALE ARE DIVIDED INTO TWO CATEGORIES; 'G' FOR GENERAL VIEW (THESE NON EXPLICIT STORIES ARE DISPLAYED ON THE HOMEPAGE OF NON-AUTHENTICATED AND AUTHENTICATED USERS BELOW THE AGE OF 18). 'R' FOR RESTRICTED (THESE EXPLICIT STORIES ALONG WITH 'G' RATED STORIES ARE DISPLAYED ON THE HOME PAGE OF AUTHENTICATED USERS ABOVE THE AGE OF 18).\n\n FOR AUTHENTICATED USERS, ALL STORIES DISPLAYED ON THEIR HOME PAGE ARE FILTERED BY THE GENRE THEY ARE INTERESTED IN AS INDICATED IN THEIR USERPROFILE.\n\n  OTHER CATEGORIES OF STORIES DISPLAYED ARE THE TOP 10 LATEST AND FAVORITE STORIES ALSO STORIES WRITTEN BY THE USERS THE REQUEST_USER IS FOLLOWING.\n\n NOTE: STORIES WRITTEN BY THE REQUEST_USER IS NOT DISPLAYED ON THEIR HOMEPAGE.",tags=['Home Page'] )

    ###### DISPLAY OF STORIES RATED 'G'(General audience) FOR NON-AUTHENTICATED USERS 
    def get(self, request:Request):
        ### LOGIC FOR NON AUTHENTICATED USERS:
        if not self.request.user.is_authenticated:
            stories = Stories.objects.filter(
            contentview = 'G',
                ).distinct()


            ###### SIDE PANEL FOR LATEST STORIES 
            latest_story = Stories.objects.filter(
                contentview = 'G',
            ).distinct().order_by('-pub_date')[0:10]

            latest_serializer = StoriesSerializer(instance=latest_story, many=True)
            serializer = StoriesSerializer(instance=stories, many=True)
            response = {
        "MESSAGE" : "Stories for non authenticated users",
        "STORIES":serializer.data,
        "LATEST_STORIES_SERIALIZER":latest_serializer.data,}  

            return Response(data = response, status = status.HTTP_200_OK )
        

        ### LOGIC FOR AUTHENTICATED USERS:
        else:
            userr = Userprofile.objects.filter(user = self.request.user)

    ####### THE DISPLAY OF 'G' (General audience) RATED STORIES FOR AUTHENTICATED USERS UNDER 18 WITH SRORIES GENRES SIMILIAR TO THOSE IN THEIR PROFILE.
            if userr:
                if self.request.user.is_authenticated and self.request.user.user_profile.age < 18:

                    stories = Stories.objects.filter(
                        contentview = 'G',
                        genre__in = userr.values_list('interested_genres')
                        ).exclude(author=request.user).distinct()


                    ##### 'G' RATED STORIES BY USERS YOU FOLLOW :
                    follower = Follow.objects.filter(requestt_user=request.user)
                    stories_by_followed_user = Stories.objects.filter(
                        author__in = follower.values_list('other_user'),
                        contentview = 'G',
                    )


                    ###### SIDE PANEL FOR TOP 10 LATEST STORIES WITHIN THE REQUEST_USERS'S GENRE THAT IS RATED 'G' 
                    latest_story = Stories.objects.filter(
                        contentview = 'G',
                        genre__in = userr.values_list('interested_genres')
                        ).exclude(author=request.user).distinct().order_by('-pub_date')[0:10]


            ###### SIDE PANEL FOR TOP 10 FAVORITE (MOST LIKED) STORIES WITHIN THE REQUEST_USERS'S GENRE THAT IS RATED 'G'
                    favorite_stories = Stories.objects.annotate(
                        number_of_likes=Count("liked_post__liker")
                        ).filter(
                        number_of_likes__gt = 0,
                        genre__in = userr.values_list('interested_genres'),
                        contentview = 'G',
                        ).exclude(
                        author=request.user
                        ).order_by("-number_of_likes")[0:10]


                    latest_serializer = StoriesSerializer(instance=latest_story, many=True)
                    serializer = StoriesSerializer(instance=stories, many=True)
                    followed_stories_serializer = StoriesSerializer(instance=stories_by_followed_user, many=True)
                    favorite_stories_serializer = StoriesSerializer(instance=favorite_stories, many=True)

                    response = response = {
                        "MESSAGE" : "Stories for authenticated users below 18",
                        "STORIES":serializer.data,
                        "LATEST_STORIES_SERIALIZER":latest_serializer.data,
                        "FOLLOWED_USERS_STORY":followed_stories_serializer.data,
                        "FAVORITE_STORIES_SERIALIZER":favorite_stories_serializer.data
                    }
                    return Response(data = response, status = status.HTTP_200_OK )



    ###### THE DISPLAY OF 'G'(General audience) and 'R'(Restricted) STORIES FOR USERS ABOVE 18 WITH SRORIES GENRES  SIMILIAR TO THOSE IN THEIR PROFILE.
                elif self.request.user.is_authenticated and self.request.user.user_profile.age >= 18:

                    stories = Stories.objects.filter(
                        genre__in = userr.values_list('interested_genres')
                        ).exclude(author=request.user).distinct()


                    ###### SIDE PANEL FOR LATEST STORIES WITH NO RESTRICTIONS
                    latest_story = Stories.objects.filter(
                        genre__in = userr.values_list('interested_genres')
                        ).exclude(author=request.user).distinct().order_by('-pub_date')[0:10]

                    ######## STORIES BY USERS YOU FOLLOW 
                    follower = Follow.objects.filter(requestt_user=request.user)
                    stories_by_followed_user = Stories.objects.filter(
                        author__in = follower.values_list('other_user'),
                    )


                    ###### SIDE PANEL FOR TOP 10 FAVORITE (MOST LIKED) STORIES WITHIN THE REQUEST_USERS'S GENRE WITH NO ###### RESTRICTIONS:
                    favorite_stories = Stories.objects.annotate(
                        number_of_likes=Count("liked_post__liker")
                        ).filter(
                        number_of_likes__gt = 0,
                        genre__in = userr.values_list('interested_genres'),
                        ).exclude(
                        author=request.user
                        ).order_by("-number_of_likes")[0:10]


                    latest_serializer = StoriesSerializer(instance=latest_story, many=True)
                    serializer = StoriesSerializer(instance=stories, many=True)
                    followed_stories_serializer = StoriesSerializer(instance=stories_by_followed_user, many=True)
                    favorite_stories_serializer = StoriesSerializer(instance=favorite_stories, many=True)


                    response = response = {
                        "MESSAGE" : "Stories for authenticated users above 18 ",
                        "STORIES":serializer.data,
                        "LATEST_STORIES_SERIALIZER":latest_serializer.data,
                        "FOLLOWED_USERS_STORY":followed_stories_serializer.data,
                        "FAVORITE_STORIES_SERIALIZER":favorite_stories_serializer.data
                    }

                    return Response(data = response, status = status.HTTP_200_OK )

            else:
                return Response({'Message': 'No Userprofile Created!'}, status = status.HTTP_400_BAD_REQUEST)


############
##### LIST OF ALL GENRES:
############

class AllGenres(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(operation_summary="Get the list of all genres", operation_description="THESE ARE THE GENRE CLASSIFICATION OF STORIES IN TINKERTALE", tags=['Genres'])

    def get(self, request:Request):
        all_genres = Genre.objects.all()
        serializer = GenreSerializer(instance=all_genres, many=True)
        response = {
            "MESSAGE": "THESE ARE THE LIST OF ALL GENRES",
            "GENRES": serializer.data
        }
        return Response(data = response, status = status.HTTP_200_OK)



############
##### CATEGORIZATION OF STORIES BY GENRE
############:

class StoriesByGenre(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(operation_summary="Get stories by genre", tags=['Genres'], )

    def get(self, request:Request, genre):
        genres = Genre.objects.get(genre=genre)
        stories = Stories.objects.filter(genre=genres)
        stories_serializer = StoriesSerializer(instance=stories, many=True)

        response = {
            "MESSAGE": "These are the stories in the genre selected",
            "STORIES": stories_serializer.data
        }

        return Response(data = response, status = status.HTTP_200_OK )



###########
##### WRITING OF NEW STORIES
###########:

class WriteStories(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StoriesSerializer
    query_set = Stories

    @swagger_auto_schema(operation_summary="Write new stories", operation_description="THE AGE RATING(CONTENT VIEW) OF THE STORIES MUST BE INDICATED; 'G' FOR GENERAL AUDIENCE(FOR READERS BELOW THE AGE OF 18) AND 'R' FOR RESTRICTED VIEW(FOR AUTHENTICATED USERS ABOVE THE AGE OF 18)", request_body= StoriesSerializer, tags=['Stories'])

    def post(self, request:Request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save(author=self.request.user)

            response = {
                "MESSAGE":"Story Created!!!",
                "STORY":serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



############
###### LOGIC TO RETRIEVE STORIES:
############

class RetrieveUpdateStories(APIView):
    permission_classes = [permissions.IsAuthenticated]


    @swagger_auto_schema(operation_summary="Retrieve a story",operation_description="THIS ENDPOINT RETRIEVES A STORY WITH ITS COMMENTS AND ALSO A RECOMMENDATION OF USERS(THAT ARE AUTHORS) TO FOLLOW WHOSE GENRE OF STORIES WRITTEN IS SIMLIAR TO THE REQUEST_USER'S INTERESTED GENRE.", tags=['Stories'])

    def get(self, request:Request, story_slug):
        stories = Stories.objects.get(slug=story_slug)
        serializer = StoriesSerializer(instance = stories )


        ### View all comments on a story:
        comments = Comment.objects.filter(story = stories)
        comment_serialzer = CommentSerializer(instance=comments, many=True)


        ####### WHO TO FOLLOW:
        ####### Recommendation of users who have written stories(that are authors) whose genre in profile is similiar to that in users profile:
        userr = Userprofile.objects.values_list('interested_genres').filter(user=request.user).distinct()
        
        user_with_story = User.objects.filter(
            story_author__isnull = False,
            story_author__genre__in = userr).exclude(username=request.user)
        
        to_follow = Userprofile.objects.filter(
            user__in = user_with_story
            )
        
        to_follow_serializer = ToFollowSerializer(instance=to_follow, many=True)
        
        response = {
                "MESSAGE":"Detail on story requested",
                "STORY":serializer.data,
                "COMMENTS": comment_serialzer.data,
                "WHO_TO_FOLLOW":to_follow_serializer.data,
            }

        return Response(data=response, status=status.HTTP_200_OK)
    

    ##### ALLOW USERS TO UPDATE THEIR STORIES:
    @swagger_auto_schema(operation_summary="Edit stories", request_body=StoriesSerializer, tags=['Stories'])

    def put(self, request:Request, story_slug):
        stories = Stories.objects.get(slug=story_slug)
        if request.user == stories.author:
            data = request.data
            serializer = StoriesSerializer(instance = stories,data = data)

            if serializer.is_valid():
                serializer.save()

                response={
                    "MESSAGE": "Story Updated Successfully!!!",
                    "STORY":serializer.data
                }


                return Response(data=response, status=status.HTTP_200_OK)

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        return Response({'Message': 'Not allowed: You are not the author of this story!'},status=status.HTTP_406_NOT_ACCEPTABLE)


    ##### ALLOW OTHERS TO COMMENT ON STORIES:
    @swagger_auto_schema(operation_summary="Comment on a story", request_body=CommentSerializer, tags=['Stories'])

    def post(self, request:Request, story_slug):
        stories = Stories.objects.get(slug=story_slug)
        data = request.data
        serializer = CommentSerializer(data = data)

        if serializer.is_valid():
            serializer.save(user=request.user,story=stories)

            response = {
                "MESSAGE":"Comment Created!!!",
                "COMMENT":serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#############
###### LIKE LOGIC FOR STORIES:
#############

class LikeLogic(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_summary="Like stories by user", tags=['Like/Dislike'])

    def get(self, request:Request, story_slug):
        stories = Stories.objects.get(slug=story_slug)
        liker = request.user
        already_liked = Like.objects.filter(story=stories, liker=liker)

        if not already_liked:
            liked_story = Like(story=stories, liker=liker)
            liked_story.save()
            serializer = LikeSerializer(instance=liked_story)

            response = {
                "MESSAGE":"You liked this story!!!",
                "LIKE":serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response({'Message': 'You have liked this user!'},status=status.HTTP_400_BAD_REQUEST)



#############
###### UN-LIKE LOGIC FOR STORIES:
#############

class UnlikeLogic(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_summary="Dislike stories by user", tags=['Like/Dislike'])

    def delete(self, request:Request, story_slug):
        stories = Stories.objects.get(slug=story_slug)
        liker = request.user
        already_liked = Like.objects.filter(story=stories, liker=liker)
        already_liked.delete()

        return Response({"MESSAGE": "You just disliked this story"},status=status.HTTP_200_OK)


