# TinkerTale
Deployed Live API Documentation here: https://tinkertale.up.railway.app/docs/

TinkerTale is a REST API that offers amazing possibilities for webapps that are dedicated to story telling. It provides features like age-based restrictions on the content users can view, a storytelling competition where the highest voted stories are elevated to a prestigious list and a variety of other features like archiving stories, restriction of stories for non authenticated users and many more.

The stories created by users are are under two categories: 'G' for General View(For readers below the age of 18) and 'R' for Restricted(For readers above the age of 18)

Below is the list of all genres of stories written in TinkerTale:
- Fiction
- Historical-Fiction
- Mystery
- Horror
- Fantasy
- Thriller
- Romance
- Drama
- Adventure
- Humor
- Poetry
- Paranormal
- Fan-Fiction
- Non-Fiction

  # Features

  GENERAL:
  - Regulation of content in users homepage i.e rendering of 'G' rated stories for Non-Authneticated and Authenticated users below the age of 18 and display of 'G' and 'R' rated stories for Authenticated users above the age of 18, for authenticated users, stories displayed are filtered on the basis of the genres they are interested in as indicated in their userprofile
  - Display of Top 10 Favorite and Latest stories also with stories by users you follow
  - Creation of stories with their content rating cumpolsorily added by the authors
  - A detail page for for each story that displays a reccomendation of authors whose genre of stories written are similiar to those that request user is intersted in
  - Users can like, dislike, comment o stories, they also can edit their stories
  - Users can archive stories
  - Users can follow and unfollow other users, they can also retrieve a list of their followers and of those they follow
  - Signing-up, Signing-in and Register of Users
  - Creation and Updating of Userprofiles
  - Display of Userprofiles with stories they have liked and written

  STORY CHALLENGE:
  - Users can submit stories for say a biweekly challenge with the highest voted stories elevated to a prestigious list; The Emerald List


# Installation and Usage
1. Clone the repository

``` $ git clone https://github.com/AyobomiOmojola/ProAssist.git ```

3. Comment out the production PostgreSQL database in the settings file and replace with SQLlite for use in development
   
5. Repeat the above step also for redis and have a redis docker container running on your local machine
   
7. Create and activate a virtual environment for this project

``` $ python -m venv venv ```

``` $ source venv/bin/activate ```

6. Install project dependencies

``` $ pip install -r requirements.txt ```

8. Run database migrations
   
``` $ py manage.py migrate ```

10. Create superuser to access the admin dashboard
    
``` $ py manage.py createsuperuser ```

12. Run the development server
    
``` $ py manage.py runserver ```

13. Access the live API documentation at ```http://127.0.0.1:8000/docs```
    
14. Where USERNAME = Username of the user you want to chat with and TOKEN = Your Login Token;
    
Hence access the chat server at ```http://127.0.0.1:8000/USERNAME/?token=TOKEN```

(You could register and login users and follow the url guide above to correctly load their chat screens on say two different browser tabs)

# Authors
ProAssist is developed and maintained by Ayo Omojola
