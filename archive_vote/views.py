from rest_framework.decorators import APIView 
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, permissions
from core_app.models import Stories
from drf_yasg.utils import swagger_auto_schema
from .models import ReadLater, StoryForChallenge, StoryWriteUpChallenge, VoteForStories, EmeraldList
from .serializers import ReadLaterSerializer, StoryForChallengeSerializer, BiWeeklyChallengeSerializer, VoteForStoriesSerializer, EmeraldListSerializer
from django.db.models import Count

# Create your views here.

###########
#### LOGIC FOR THE BIWEEKLY CHALLENGE:
###########

class CreateStoryChallenge(APIView):
    permission_classes = [permissions.IsAuthenticated]
    ###### CREATE THE BIWEEKLY CHALLENGE:
    @swagger_auto_schema(operation_summary="Create the biweekly challenge", operation_description="THIS ENDPOINT ALLOWS AN ADMIN USER TO CREATE THE CONTEXT FOR STORIES TO BE SUBMITTED FOR A BIWEEKLY CHALLENGE (NOTE: FOR THE SAKE OF TESTING THIS ENDPOINT AUTHENTICATED, USERS ARE ALLOWED TO DO SO)", request_body=BiWeeklyChallengeSerializer, tags=['BiWeekly Challenge'])

    def post(self, request:Request):
        data = request.data
        serializer = BiWeeklyChallengeSerializer(data=data)

        if serializer.is_valid(): 
            serializer.save()

            response = {
                "MESSAGE":"Context for the biweekly story challenge created!",
                "STORIES_CONTEXT":serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    

    #### GET THE CONTEXT OF STORIES TO BE WRITTEN FOR THE BIWEEKLY STORY CHALLENGE:
    @swagger_auto_schema(operation_summary="Get the latest biweekly context for stories", operation_description="THIS ENDPOINT ALLOWS USERS TO GET THE LATEST STORY-CONTEXT OF STORIES TO BE SUBMITTED FOR A BIWEEKLY CONTEST WITH THE HIGHEST VOTED STORY ELEVATED TO THE EMERALD LIST.", tags=['BiWeekly Challenge'])

    def get(self, request:Request):
        try:
            get_challenge = StoryWriteUpChallenge.objects.all().order_by('-pub_date')[0]
            serializer = BiWeeklyChallengeSerializer(instance = get_challenge)

            response = {
                "MESSAGE": "This is the Biweekly challenge",
                "BIWEEKLY_CHALLENGE":serializer.data
            }

            return Response(data=response, status=status.HTTP_200_OK)
        
        except IndexError:
            return Response({'Message': 'There is no story challenge written!'}, status = status.HTTP_400_BAD_REQUEST)


########
### LOGIC FOR STORIES FOR THE BIWEEKLY CHALLENGE:
########

class StoryForChallengeLogic(APIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    ##### GET ALL THE STORIES WRITTEN FOR THE BIWEEKLY STORY CHALLENGE:
    @swagger_auto_schema(operation_summary="Get all stories submitted for challenge", operation_description="THIS GETS ALL THE STORIES SUBMITTED FOR THE CHALLENGE WHILE EXCLUDING THOSE ALREADY TRANSFERRED TO THE EMERALD LIST FOR WINNING PREVIOUS BIWEEKLY CHALLENGES", tags=['BiWeekly Challenge'])

    def get(self, request:Request):
        stories = StoryForChallenge.objects.exclude(emerald_stories__isnull = False)
        serializer = StoryForChallengeSerializer(instance = stories, many=True)

        response = {
            "MESSAGE": "These are the list of all the stories for this week",
            "STORIES_SUBMITTED":serializer.data
        }

        return Response(data=response, status=status.HTTP_200_OK)


    ##### WRITE STORIES FOR THE CHALLENGE WITH THE MAXIMUM OF 20 STORIES:
    @swagger_auto_schema(operation_summary="Create stories for the biweekly challenge", operation_description="THIS ENDPOINT ALLOWS USERS TO CREATE STORIES UP FOR A BIWEEKLY CONTEST, WHOSE WINNER(THAT IS THE STORY WITH THE HIGHEST VOTE) WOULD BE PUT ON AN EMERALDLIST(THIS COULD BE EVERY TWO WEEKS, WHICH MAKES THE NUMBER OF STORIES IN THIS LIST TO BE ABOUT '26' BY THE END OF THE YEAR), SUCH STORIES WILL ONLY GET CREATED AS LONG AS THE NUMBER OF STORIES ALREADY CREATED DOES NOT EXCEED '20'.", request_body=StoryForChallengeSerializer, tags=['BiWeekly Challenge'])

    def post(self, request:Request):
        data = request.data
        serializer = StoryForChallengeSerializer(data=data)
        total_vote_stories = StoryForChallenge.objects.exclude(emerald_stories__isnull = False).count()

        if serializer.is_valid() and total_vote_stories < 20:
            serializer.save(author=self.request.user)

            response = {
                "MESSAGE":"Story Created!!!",
                "YOUR_STORY":serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)



##############
##### LOGIC TO VOTE FOR STORIES:
##############

class VoteForAStory(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_summary="Vote for stories submitted for challenge", tags=['BiWeekly Challenge'])

    def get(self, request:Request, story_slug):
        story = StoryForChallenge.objects.get(slug=story_slug)
        story_incontest = VoteForStories.objects.filter(stories=story)

        if story_incontest:
            story_incontest = VoteForStories.objects.get(stories=story)
            story_incontest.voter.add(request.user)
            serializer = VoteForStoriesSerializer(instance=story_incontest)

            response = {
                    'MESSAGE': 'You have successfully voted for this story',
                    'VOTE':serializer.data
                }

            return Response(data = response, status = status.HTTP_200_OK )
    
        else:
            create_story = VoteForStories(stories=story)
            create_story.save()
            create_story.voter.add(request.user)
            story_incontest1 = VoteForStories.objects.get(stories=story)
            serializer = VoteForStoriesSerializer(instance=story_incontest1)

            response = {
                    'MESSAGE': 'You have successfully voted for this story',
                    'VOTE':serializer.data
                }

            return Response(data = response, status = status.HTTP_200_OK )


############
###### LOGIC FOR THE EMERALD LIST:
############

class EmeraldStoryWinner(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_summary="Display all strories on the Emerald List", tags=['BiWeekly Challenge'])
#### GET ALL STORIES ON THE EMERALD LIST
    def get(self, request:Request):
        emerald_list = EmeraldList.objects.all()
        serializer = EmeraldListSerializer(instance=emerald_list, many = True)

        response = {
            "MESSAGE": "These are all the stories on the Emerald List",
            "EMERALD_LIST_STORIES": serializer.data
        }

        return Response(data = response, status=status.HTTP_200_OK)


#### TRANSFER THE HIGHEST VOTED STORY TO AN EMERALD LIST WHILE DELETING THE REST
    @swagger_auto_schema(operation_summary="Transfer highest voted story to an Emerald List", operation_description="THIS ENDPOINT ALLOWS A TINKERTALE ADMIN USER(NOTE: FOR THE SAKE OF TESTING THIS ENDPOINT, AUTHENTICATED USERS ARE ALLOWED TO DO SO) TO TRANSFER THE HIGHEST VOTED STORY SUBMITTED FOR THE BIWEEKLY CONTEST WHILE SIMULTANOEUSLY DELETING THE REST.", tags=['BiWeekly Challenge'])

    def delete(self, request:Request):
        story = StoryForChallenge.objects.all()
        if story:
            maximum_voted_story = StoryForChallenge.objects.exclude(
                emerald_stories__isnull = False
            ).annotate(
            count_vote = Count("genre_vote_stories__voter")
            ).values_list(
                "genre_vote_stories"
            ).order_by(
                "-count_vote"
            )[0]


            if maximum_voted_story != (None,): 
                StoryForChallenge.objects.exclude(
                    genre_vote_stories__in = maximum_voted_story,
                    ).exclude(emerald_stories__isnull = False).delete()

                winner = StoryForChallenge.objects.exclude(emerald_stories__isnull = False)[0]
                challenge_winner = EmeraldList(stories=winner)
                challenge_winner.save()
                serializer = EmeraldListSerializer(instance = challenge_winner)

                response = {
                "MESSAGE":"You have Succesfully deleted all but the Highest voted story and transferred it to the Emerald List",
                "EMERALD_LIST_STORIES":serializer.data
                    }
                return Response(data = response, status=status.HTTP_200_OK)

            else:
                return Response(
                {'Message': 'There are no voted stories!'}, 
                status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'Message': 'There are no stories to transfer!'}, 
                status = status.HTTP_400_BAD_REQUEST)




##############
###### LOGIC TO ALLOW USERS TO ARCHIVE STORIES:
##############

class AddToArchive(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(operation_summary="Archive a story", tags=['Archive'])

    def get(self, request:Request, story_slug):
        storiess = Stories.objects.get(slug = story_slug)
        archive_user = ReadLater.objects.filter(owner=request.user)

        if archive_user:
            archive_user = ReadLater.objects.get(owner=request.user)
            archive_user.stories.add(storiess)
            serializer = ReadLaterSerializer(instance=archive_user)
            response = {
                'MESSAGE': 'You just successfully archived this story',
                'ARCHIVED_STORY':serializer.data
            }
            return Response(data = response, status = status.HTTP_200_OK )
        
        else:
            read_later = ReadLater(owner=request.user)
            read_later.save()
            read_later.stories.add(storiess)
            archive_user1 = ReadLater.objects.get(owner=request.user)
            serializer = ReadLaterSerializer(instance=archive_user1)

            response = {
                'MESSAGE': 'You just archived this story!',
                'ARCHIVED_STORY':serializer.data
            }
            return Response(data = response, status = status.HTTP_200_OK )


##############
###### LOGIC TO GET ALL ARCHIVED STORIES BY USER:
##############

class GetArchivedStories(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_summary="Get all your archived stories", tags=['Archive'])

    def get(self, request:Request):
        archived_stories = ReadLater.objects.filter(owner=request.user)
        archived_serializer = ReadLaterSerializer(instance=archived_stories, many=True)

        response = {
                'MESSAGE': 'These are your archived stories',
                'ARCHIVED_STORIES':archived_serializer.data
            }
        
        return Response(data = response, status = status.HTTP_200_OK )