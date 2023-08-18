from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics, status
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class RoomView(generics.ListAPIView):

    # Show all rooms
    queryset = Room.objects.all()

    # Define serializer class
    serializer_class = RoomSerializer


class GetRoomView(APIView):

    # Define serializer class variables to serialize data
    serializer_class = RoomSerializer

    def get(self, request, format=None):

        # Query database to look up for the room with this code
        room = Room.objects.filter(code=request.GET.get("code")).first()

        # Check if the room is exist in database
        if room:

            # Serialize/Convert data from the Room queryset to Python datatype to be rendered into JSON,...
            data = RoomSerializer(room).data

            # Check if the user is the room host
            data['is_host'] = self.request.session.session_key == room.host

            # Update room code for user session
            self.request.session["room_code"] = room.code

            # Return data with OK status
            return Response(data, status=status.HTTP_200_OK)

        # Return response with no result found based on the room code
        return Response({"Room Not Found": "Invalid Room Code"}, status=status.HTTP_404_NOT_FOUND)


class JoinRoomView(APIView):

    def post(self, request, format=None):

        # Check if user has session key
        if not self.request.session.exists(self.request.session.session_key):

            # Create session key for user
            self.request.session.create()

        # Query database and filter to lookup for the room
        room = Room.objects.filter(code=request.data.get("code")).first()

        # Check if the room is exist
        if room:

            # Update room code for user session
            self.request.session["room_code"] = room.code

            # Return successful response
            return Response({"Message":"Room Joined"}, status=status.HTTP_200_OK)

        # Return response with no result found based on the room code
        return Response({"Room Not Found": "Invalid Room Code"}, status=status.HTTP_404_NOT_FOUND)


class CreateRoomView(APIView):

    # Define serializer class variables to serialize data
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):

        # Check if user has session key
        if not self.request.session.exists(self.request.session.session_key):

            # Create session key for user
            self.request.session.create()

        # Serialize/Convert all the data using serializer class to get Python datatype
        serializer = self.serializer_class(data=request.data)

        # Validate the serializer data
        if serializer.is_valid():

                # Create new room for the host
                new_room = Room(
                    host=self.request.session.session_key,
                    guest_can_pause=serializer.data.get("guest_can_pause"),
                    votes_to_skip=serializer.data.get("votes_to_skip"),
                )

                # Save the new room object to the database
                new_room.save()

                # Update room code for user session
                self.request.session["room_code"] = new_room.code

                # Return with Successful Created response for user request
                return Response(RoomSerializer(new_room).data, status=status.HTTP_201_CREATED)

        # Return Bad Request Response if the data is invalid
        return Response({"Bad Request": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


class UserInRoomView(APIView):

    def get(self, request, format=None):

        # Check if user has session key
        if not self.request.session.exists(self.request.session.session_key):

            # Create session key for user
            self.request.session.create()

        # Get info for the user session about the room code user had joined
        data = {
            "code": self.request.session.get("room_code")
        }

        # Return Json object
        return JsonResponse(data, status=status.HTTP_200_OK)


class LeaveRoomView(APIView):

    def post(self, request, format=None):

        # Check if user is in a room
        if "room_code" in self.request.session:

            # Remove room from the user session
            self.request.session.pop("room_code")

        # Return successful OK response
        return Response({"Message": "Room Left"}, status=status.HTTP_200_OK)


class DeleteRoomView(APIView):

    def post(self, request, format=None):

        # Check if user is in a room
        if "room_code" in self.request.session:

            # Lookup for the room that the host want to delete then delete it
            Room.objects.filter(code=self.request.session.get("room_code")).first().delete()

            # Remove room from the user session
            self.request.session.pop("room_code")

        # Return successful OK response
        return Response({"Message": "Room Deleted"}, status=status.HTTP_200_OK)


class UpdateRoomView(APIView):

    # Define serializer class variable
    serializer_class = UpdateRoomSerializer

    def patch(self, request, format=None):

        # Check if user has session key
        if not self.request.session.exists(self.request.session.session_key):

            # Create session key for user
            self.request.session.create()

        # Passing data to serialize/convert to Python datatype
        serializer = self.serializer_class(data=request.data)

        # Validate data
        if serializer.is_valid():

            # Lookup the room with room code
            room = Room.objects.filter(code=serializer.data.get("code")).first()

            # Check if the room is exist and if the user is the host of the room
            if room and room.host == self.request.session.session_key:

                # Update the info of the room
                room.guest_can_pause = serializer.data.get("guest_can_pause")
                room.votes_to_skip = serializer.data.get("votes_to_skip")

                # Save the room update
                room.save(update_fields=["guest_can_pause", "votes_to_skip"])

                # Return data with OK status
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)

            # If user is not the host, return message that they are not allowed to change
            return Response({"Message":"Only host can make changes"}, status=status.HTTP_403_FORBIDDEN)

        # If serializer is not valid, return message that data is invalid
        return Response({"Bad Request": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


class MyRoomView(APIView):

    def get(self, request, format=None):

        # Check if user has session key
        if not self.request.session.exists(self.request.session.session_key):

            # Create session key for user
            self.request.session.create()

        # Query to get all the rooms of current user
        my_rooms = Room.objects.filter(host=self.request.session.session_key)

        # Return room data in response
        return Response(RoomSerializer(my_rooms, many=True).data, status=status.HTTP_200_OK)


class MyPlaylistView(APIView):

    def get(self, request, format=None):

        # Check if user has session key
        if not self.request.session.exists(self.request.session.session_key):

            # Create session key for user
            self.request.session.create()

        # Query to get all the rooms of current user
        my_playlist = Song.objects.filter(playlist_of=self.request.session.session_key)

        # Return room data in response
        return Response(SongSerializer(my_playlist, many=True).data, status=status.HTTP_200_OK)