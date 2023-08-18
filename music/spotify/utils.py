from .models import *
from django.utils import timezone
from datetime import timedelta
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from requests import post, put, get


BASE_URL = "https://api.spotify.com/v1/me/"


# Function to update or create tokens for user
def handle_user_tokens(session_key, access_token, refresh_token , expires_in, token_type):

    # Get the tokens associated with current user
    tokens = SpotifyToken.objects.filter(user=session_key).first()

    # Convert expires time of tokens
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    # Check if tokens is associated with current user
    if tokens:

        # Update Tokens for the current user
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=[
            "access_token",
            "refresh_token",
            "expires_in",
            "token_type",
        ])

    # Otherwise, create new Tokens for current user
    else:

        # Create new Tokens
        tokens = SpotifyToken(
            user=session_key,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
            token_type=token_type,
        )

        # Save the new Tokens
        tokens.save()


# Function to refresh new access tokens
def refresh_spotify_tokens(session_key):

    # Get the tokens associated with current user
    tokens = SpotifyToken.objects.filter(user=session_key).first()

    # Send POST method request to Spotify
    # asking for new access token using our refresh token*
    # then convert to json to get data to refresh our access token
    # *Refresh token stays the same and it is used to request a renewed access token
    response = post("https://accounts.spotify.com/api/token", data={
        "grant_type": "refresh_token",
        "refresh_token": tokens.refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }).json()

    # Calling fuction to update new access token
    handle_user_tokens(
        session_key,
        response.get("access_token"),
        tokens.refresh_token,
        response.get("expires_in"),
        response.get("token_type"),
    )


# Function handle sending request to Spotify
def handle_spotify_request(session_key, endpoint, method):

    # Get the tokens associated with current user
    tokens = SpotifyToken.objects.filter(user=session_key).first()

    # Create a form to send request to Spotify
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + tokens.access_token,
        }

    # Check if it is post request:
    if method.lower() == "post":

        # Send post request
        post(BASE_URL + endpoint, headers=headers)

    # Check if it is put request
    elif method.lower() == "put":

        # Send the put request
        put(BASE_URL + endpoint, headers=headers)

    # Otherwise, it is get request
    else:

        # Send the get request
        response = get(BASE_URL + endpoint, {}, headers=headers)

        # Try to return response with json info
        try:

            # Return response with json info
            return response.json()

        # Error handler
        except:

            # Return error message
            return {"Error": "Something wrong with your request"}

