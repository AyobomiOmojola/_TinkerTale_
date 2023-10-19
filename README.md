# TinkerTale
Deployed Live API Documentation here: https://tinkertale.up.railway.app/docs/

TinkerTale is a REST API that offers amazing possibilities for webapps that are dedicated to story telling. It provides features like age-based restrictions on the content users can view, a storytelling competition where the highest voted stories are elevated to a prestigious list and a variety of other features like archiving stories, restriction of stories for non authenticated users and many more.

The stories created by users are under two categories: 'G' for General View (For readers below the age of 18) and 'R' for Restricted (For readers above the age of 18)

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
- Regulation of content in users homepage i.e rendering of 'G' rated stories for Non-Authenticated and Authenticated users below the age of 18 and display of 'G' and 'R' rated stories for Authenticated users above the age of 18, for Authenticated users, stories displayed are filtered on the basis of the genres they are interested in as indicated in their userprofile
- Display of Top 10 favorite and latest stories also with stories by users you follow
- Creation of stories with their content rating compulsorily added by the authors
- A detail page for each story that displays a recommendation of authors whose genre of stories written are similiar to those that the request user is interested in
- Users can like, dislike and comment on stories, they can also edit their stories
- Users can archive stories
- Users can follow and unfollow other users, they can also retrieve a list of their followed users and who they are following
- Signing-up, Signing-in and Logging-out of Users
- Creation and Updating of Userprofiles
- Display of Userprofiles with stories they have liked and written


  STORY CHALLENGE:
- Users can submit stories for say a biweekly challenge with the highest voted stories elevated to a prestigious list


# Installation and Usage
1. Clone the repository

``` $ git clone https://github.com/AyobomiOmojola/_TinkerTale_.git ```

2. Comment out the production PostgreSQL database in the settings file and replace with SQLlite for use in development 
   
3. Create and activate a virtual environment for this project

``` $ python -m venv venv ```

``` $ source venv/bin/activate ```

4. Install project dependencies

``` $ pip install -r requirements.txt ```

5. Run database migrations
   
``` $ py manage.py migrate ```

6. Create superuser to access the admin dashboard
    
``` $ py manage.py createsuperuser ```

7. Run the development server
    
``` $ py manage.py runserver ```

8. Access the live API documentation at ```http://127.0.0.1:8000/docs```

# Authors
ProAssist is developed and maintained by Ayo Omojola
