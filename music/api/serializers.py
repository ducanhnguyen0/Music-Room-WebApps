from rest_framework import serializers
from .models import *


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ("id", "title", "artists")


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("id", "code", "host", "guest_can_pause", "votes_to_skip", "created_at")


class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("guest_can_pause", "votes_to_skip")


class UpdateRoomSerializer(serializers.ModelSerializer):

    # Since the code field is unique, serializer will consider it as invalid and not allow to pass in the data if we try to pass in a code that already exist
    # In order to update the room with exist room code, redefine inside this class so we can pass in the room code
    code = serializers.CharField(validators=[])

    class Meta:
        model = Room
        fields = ("code", "guest_can_pause", "votes_to_skip")
