from django.urls import path
from .views import *

urlpatterns = [
    path("authorize", Authorize.as_view()),
    path("redirect", spotify_authentication),
    path("authenticate", Authenticate.as_view()),
    path("current-song", CurrentSong.as_view()),
    path("add-song", AddSong.as_view()),
    path("play", PlaySong.as_view()),
    path("pause", PauseSong.as_view()),
    path("skip", SkipSong.as_view()),
]
