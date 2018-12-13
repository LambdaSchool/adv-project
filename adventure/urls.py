from django.conf.urls import url
from . import api

urlpatterns = [
    url("init", api.initialize),
    url("move", api.move),
    url("say", api.say),
    url("shout", api.shout),
    url("players", api.players),
    url("whisper", api.whisper),
]
