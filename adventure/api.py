from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

# instantiate pusher
pusher = Pusher(
    app_id=config("PUSHER_APP_ID"),
    key=config("PUSHER_KEY"),
    secret=config("PUSHER_SECRET"),
    cluster=config("PUSHER_CLUSTER"),
)


@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.playerNames(player_id)
    allPlayerNames = player.allPlayerNames(player_id)
    return JsonResponse(
        {
            "uuid": uuid,
            "name": player.user.username,
            "title": room.title,
            "description": room.description,
            "players": players,
            "allPlayerNames": allPlayerNames,
        },
        safe=True,
    )


# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs = {"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data["direction"]
    room = player.room()
    nextRoomID = None
    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        player.currentRoom = nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        for p_uuid in currentPlayerUUIDs:
            pusher.trigger(
                f"p-channel-{p_uuid}",
                "broadcast",
                {"message": f"{player.user.username} has walked {dirs[direction]}."},
            )
        for p_uuid in nextPlayerUUIDs:
            pusher.trigger(
                f"p-channel-{p_uuid}",
                "broadcast",
                {
                    "message": f"{player.user.username} has entered from the {reverse_dirs[direction]}."
                },
            )
        return JsonResponse(
            {
                "name": player.user.username,
                "title": nextRoom.title,
                "description": nextRoom.description,
                "players": players,
                "error_msg": "",
            },
            safe=True,
        )
    else:
        players = room.playerNames(player_id)
        return JsonResponse(
            {
                "name": player.user.username,
                "title": room.title,
                "description": room.description,
                "players": players,
                "error_msg": "You cannot move that way.",
            },
            safe=True,
        )


@csrf_exempt
@api_view(["POST"])
def say(request):
    player = request.user.player
    player_id = player.id
    data = json.loads(request.body)
    message = data["message"]
    room = player.room()
    currentPlayerUUIDs = room.playerUUIDs(player_id)

    for p_uuid in currentPlayerUUIDs:
        pusher.trigger(
            f"p-channel-{p_uuid}",
            "broadcast",
            {"message": f"{player.user.username} says {message}"},
        )
    return JsonResponse(
        {"message": f"{player.user.username} says {message}"}, safe=True, status=200
    )


@csrf_exempt
@api_view(["POST"])
def shout(request):
    player = request.user.player
    player_id = player.id
    data = json.loads(request.body)
    shout = data["shout"]
    allPlayerUUIDs = player.allPlayerUUIDs(player_id)

    for p_uuid in allPlayerUUIDs:
        pusher.trigger(
            f"p-channel-{p_uuid}",
            "broadcast",
            {"shout": f"{player.user.username} shouts {shout}"},
        )
    return JsonResponse(
        {"shout": f"{player.user.username} shouts {shout}"}, safe=True, status=200
    )


@csrf_exempt
@api_view(["GET"])
def players(request):
    player = request.user.player
    player_id = player.id
    allPlayerNames = player.allPlayerNames(player_id)
    return JsonResponse({"allPlayerNames": allPlayerNames}, safe=True, status=200)


@csrf_exempt
@api_view(["POST"])
def whisper(request):
    player = request.user.player
    data = json.loads(request.body)
    whisperTarget = data["playerName"]
    whisper = data["whisper"]
    pusher.trigger(
        f"p-channel-{whisperTarget}",
        "broadcast",
        {"whisper": f"{player.user.username} whispers: {whisper}"},
    )
    return JsonResponse(
        {"whisper": f"You whisper {whisperTarget}: {whisper}"}, safe=True, status=200
    )
