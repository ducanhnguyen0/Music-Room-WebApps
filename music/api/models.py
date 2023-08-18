from django.db import models
import string
import random

# Create your models here.

# Function to generate room code
def generate_unique_code():

    # Define the length of the code will be
    length = 8

    # Loop until we generate an unique code
    while True:

        # Try to get a code by choosing character randomly
        code = ''.join(random.choices(string.ascii_uppercase, k=length))

        # Check if the code is used or not
        if not Room.objects.filter(code=code):

            # We generated an unique code for the room so we break the loop
            break

    # Return the generated code
    return code


# Models to store song
class Song(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=50)
    artists = models.CharField(max_length=50)
    playlist_of = models.CharField(max_length=50, null=True)


# Models to store room
class Room(models.Model):
    code = models.CharField(max_length=10, default=generate_unique_code, unique=True)
    host = models.CharField(max_length=50)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    current_song = models.ForeignKey(Song, on_delete=models.CASCADE, null=True)
