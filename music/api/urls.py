from django.urls import path
from .views import *


urlpatterns = [
    path("room", RoomView.as_view()),
    path("create-room", CreateRoomView.as_view()),
    path("get-room", GetRoomView.as_view()),
    path("join-room", JoinRoomView.as_view()),
    path("user-in-room", UserInRoomView.as_view()),
    path("leave-room", LeaveRoomView.as_view()),
    path("delete-room", DeleteRoomView.as_view()),
    path("update-room", UpdateRoomView.as_view()),
    path("my-room", MyRoomView.as_view()),
    path("my-playlist", MyPlaylistView.as_view()),
]
