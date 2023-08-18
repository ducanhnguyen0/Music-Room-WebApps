from django.urls import path

from .views import index

app_name = "frontend"

urlpatterns = [
    path("", index, name=""),
    path("join", index),
    path("create", index),
    path("my-room", index),
    path("my-playlist", index),
    path("room/<str:roomCode>", index),
]
