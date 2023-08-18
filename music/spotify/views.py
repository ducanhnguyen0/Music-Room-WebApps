from django.shortcuts import render, redirect
from django.utils import timezone
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from requests import Request, post
from .utils import *
from api.models import *
from .models import *


# Create your views here.
# Spotify authentication
# Set up API endpoint to return URL that we can go to authenticate our spotify app
class Authorize(APIView):

    def get(self, request, format=None):

        # Generate URL via GET request so we can send request to this URL later
        # The URL is where user will be redirect to authorize via Spotify
        # Clarify scopes that allow user to access
        url = Request("GET", "https://accounts.spotify.com/authorize", params={
            "scope": "user-read-playback-state user-modify-playback-state user-read-currently-playing",
            "response_type": "code",
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
        }).prepare().url

        # Return URL
        return Response({"url": url}, status=status.HTTP_200_OK)


# Sending Client_id, Client_secret, grant_type, code, uri to get the tokens
# then store tokens to our database then redirect back to original app
def spotify_authentication(request, format=None):

    # Send request via post method back the Spotify account service
    # asking for 'authorization code' type to get access token, refresh token,...
    # then convert the response that we get back into json
    response = post("https://accounts.spotify.com/api/token", data={
        "grant_type": "authorization_code",
        "code": request.GET.get("code"),
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }).json()

    # Passing data to utils function to create or update tokens for user
    handle_user_tokens(
        request.session.session_key,
        response.get("access_token"),
        response.get("refresh_token"),
        response.get("expires_in"),
        response.get("token_type"),
    )

    # Redirect back to frontend app page(original app page)
    return redirect("frontend:")


# Return response to check if user authenticated
class Authenticate(APIView):

    def get(self, request, format=None):

        # Check if user is authenticated
        # Set variables to False since the tokens are either nonexpired or invalid
        authenticated = False

        # Get the tokens associated with current user
        tokens = SpotifyToken.objects.filter(user=self.request.session.session_key).first()

        # Check if tokens is associated with current user
        if tokens:

            # Check if tokens had expired
            if tokens.expires_in <= timezone.now():

                # Calling function to refresh the tokens
                refresh_spotify_tokens(self.request.session.session_key)

            # Set variables to True since we either refresh token successfully or token is still valid
            authenticated = True

        # Return Resposne
        return Response({"status": authenticated}, status=status.HTTP_200_OK)


# Get the current playing song info
class CurrentSong(APIView):

    def get(self, request, format=None):

        # Look up for the current room
        room = Room.objects.filter(code=self.request.session.get("room_code")).first()

        # Check if room is exist or not
        if room:

            # Define endpoint
            endpoint = "player/currently-playing"

            # Use function to send request to Spotify
            response = handle_spotify_request(room.host, endpoint, "get")

            # Check if the response is valid that it has info of the song
            if "item" in response:

                # Get the data of the song
                data = response.get("item")

                # Handle case where we have multiple artists, we clean the format
                # Create our own string for artists
                artists_list = ", ".join(artist.get("name") for artist in data.get("artists"))

                # Get number of votes for the current song
                votes = Vote.objects.filter(room=room, song=room.current_song).count()

                # Create object to send to frontend
                song = {
                    "title": data.get("name"),
                    "artist": artists_list,
                    "duration": data.get("duration_ms"),
                    "time": response.get("progress_ms"),
                    "image_url": data.get("album").get("images")[0].get("url"),
                    "is_playing": response.get("is_playing"),
                    "votes": votes,
                    "votes_required": room.votes_to_skip,
                    "id": data.get("id"),
                }

                # Check if song is in database or not
                if not Song.objects.filter(id=song["id"]).first():

                    # Create new Song object and save it to database
                    Song(
                        id=song["id"],
                        title=song["title"],
                        artists=artists_list,
                    ).save()

                # Check if the song had changed
                if not room.current_song or room.current_song.id != song["id"]:

                    # Update the current song to the new song
                    room.current_song = Song.objects.filter(id=song["id"]).first()
                    room.save(update_fields=["current_song"])

                    # Remove votes for the previous song to reset the votes
                    Vote.objects.filter(room=room).delete()

                # Return our object to frontend
                return Response(song, status=status.HTTP_200_OK)

            # Return response with no content status
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        # Return response with not found status
        return Response({}, status=status.HTTP_404_NOT_FOUND)


# Handle Add song to playlist of current user
class AddSong(APIView):

    def post(self, request, format=None):

        # Lookup for the current room
        room = Room.objects.filter(code=self.request.session.get("room_code")).first()

        # Add the current song playing in the room to current user playlist
        room.current_song.playlist_of = self.request.session.session_key

        # Save the update
        room.current_song.save(update_fields=["playlist_of"])

        # Return response
        return Response({"Message": "Song Added"}, status=status.HTTP_200_OK)


# Handle Play song
class PlaySong(APIView):

    def put(self, request, format=None):

        # Lookup for the current room
        room = Room.objects.filter(code=self.request.session.get("room_code")).first()

        # Check if user is allowed to pause the song or it is the room host
        if self.request.session.session_key == room.host or room.guest_can_pause:

            # Call function to pause song
            handle_spotify_request(room.host, "player/play", "put")

            # Return response with no content status
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        # Return response with forbidden status
        return Response({}, status=status.HTTP_403_FORBIDDEN)


# Handle Pause song
class PauseSong(APIView):

    def put(self, request, format=None):

        # Lookup for the current room
        room = Room.objects.filter(code=self.request.session.get("room_code")).first()

        # Check if user is allowed to pause the song or it is the room host
        if self.request.session.session_key == room.host or room.guest_can_pause:

            # Call function to pause song
            handle_spotify_request(room.host, "player/pause", "put")

            # Return response with no content status
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        # Return response with forbidden status
        return Response({}, status=status.HTTP_403_FORBIDDEN)


# Handle skip song
class SkipSong(APIView):

    def post(self, request, format=None):

        # Lookup for the current room
        room = Room.objects.filter(code=self.request.session.get("room_code")).first()

        # Get all the votes for the current song
        votes = Vote.objects.filter(room=room, song=room.current_song)

        # Check if current user is the host or there are enough votes to skip the song
        if room.host == self.request.session.session_key or votes.count() + 1 >= room.votes_to_skip:

            # Clear all the votes of previous song
            votes.delete()

            # Call the function to skip song
            handle_spotify_request(room.host, "player/next", "post")

        # Otherwise, we register the votes
        else:

            # Create a new Vote
            vote = Vote(
                user=self.request.session.session_key,
                room=room,
                song=room.current_song
            )

            # Save the Vote
            vote.save()

        # Return response with no content status
        return Response({}, status=status.HTTP_204_NO_CONTENT)

