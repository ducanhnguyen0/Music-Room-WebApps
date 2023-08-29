# Music Room Web Application

Harvard CS50 Web Project\
Video Demo: https://youtu.be/NBIMxUR8SwE

## Description:
A fullstack django-react music web application integrating with Spotify API where users can become a DJ to host an online party or just simply listen to music with friends at the same time. Users can join others rooms to listen to their playlists or they can create their own room to play their own music to not only friends but others as well. The Music Room web application creates a new fun exciting experience for users by letting them discover the world of music of different people where they can enjoy a song that they might never heard about it or sharing the same emotion, mood through the song in the room hosted by others.


## Tech Stack:

* Python
* Django
* Rest Framework
* JavaScript
* React
* Node.js

## Distinctiveness and Complexity:

* Distinctiveness:
This project is different from other projects in the course since the project itself is involving with music experience which is different from other projects and also, the features fo the web app is also unique in comparision with other projects in the course. The web app allow user to create different rooms with specification for the room or join others room instead of creating your own room. The web app allow users to play their music playlists via Spotify API and allow others in the room to listen together and if there is a song user like, user can add to their own playlist in the web app. The web app focus on how to improve music experience for users rather than selling product or interaction like e-commerce or social network project. That is why I believe
this web project is distinct from other projects in the course because of the web app features.

* Complexity:
Unlike other project in the course where we simply using django to handle logic in backend and render the page with html, css, javascript but this project itself contains three different components to build a complete web application. Music Room web app ultilize Django to handle logic and models of database for the backend but also using Rest framework to create API View that allow others frontend app using API to the backend server which is more complex since it requires to handle more logic and how send data back to the frontend who request to the server. Besides, this web app using react and node modules for the frontend which contains a lot of new syntaxs and it is more complex on how to handle routing logic in the frontend parts. Moreover, Music Room also integrates Spotify API to fetch song data from Spotify Server which requires the web app to handle with Spotify authentication and authorization. Based on all of these different parts of web application, I believe this project satisfies the complexity requirements.


## Project Specification:

### api
The app resposible for handling backend of the web app. In the api app, there are multiple main files:

* models.py:
Models of the backend storing room and song

* serializers.py:
Serializer for API View to transform data type

* urls.py:
Paths of the backend API

* views.py:
API View logic in backend server contains several functions handle request to get room, join room, create room, update room, my room, my playlist.

### frontend
The app resposible for handling frontend of the web app. In the frontend app, there are multiple main folder, files:

* src:
JavaScript files which handle the UI of the web app page

* static:
Storing css style files and main javacript files

* templates:
HTML layout of the web app

* urls.py:
Paths of all pages in web app for routing

* views.py:
Render the html page

*Other folders and files contains dependencies from node modules

### spotify
The app resposible for handling Spotify API. In the spotify app, there are multiple main files:

* models.py:
Models for storing tokens of spotify and votes

* credentials.py:
Storing credetials of app to Spotify API

* urls.py:
Paths of the backend API

* utils.py:
Helper function to handle tokens and request from Spotify API

* views.py:
API View Logic in backend server contains several functions handle spotify api authentication, authorization, request.



## How to run

### Install Python packages

pip install -r requirements.txt

### [Install Node.js](https://nodejs.org)

### Install Node Modules

1. Change directory to frontend app
   ```
   cd frontend
   ```
2. Install node dependencies:
   ```
   npm i
   ```
   (You might need to add ```--legacy-peer-deps``` or ```--force``` since the dependencies are old versions)
3. Compile:
   ```
   npm run build
   ```
   For development:
   ```
   npm run dev
   ```

### Register Spotify account and Create App in Development Dashboard

1. URI: (your local host)/redirect
2. Get the Client ID, Client Secret and replace that in credentials.py file inside spotify app
*Note: You need Spotify Premium to use play, pause, skip features inside web app(You can still play, pause, skip in spotify and web app acts the same)

### Run Django Web Server

1. Change directory to main app:
   ```
   cd music
   ```
2. Initialize the database:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Run the app locally:
   ```
   python manage.py runserver
   ```
