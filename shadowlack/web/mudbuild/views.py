# Views for our character app

from django.http import Http404
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

from typeclasses.rooms import Room

from evennia.utils import class_from_module
from evennia.utils.search import object_search
from evennia.utils.utils import inherits_from


def room_map(request):

    Room = class_from_module(settings.BASE_ROOM_TYPECLASS)
    rooms = Room.objects.filter().values()

    return render(request, 'rooms/map.html', {
        'object_list': rooms
        })


# outdoor_rooms = Room.objects.get_by_tag("outdoors", category="room_type")

# outdoor_rooms_with_players = outdoor_rooms.filter(locations_set__db_typeclass_path="typeclasses.characters.Character")
# is_outdoors = myroom.tags.get("outdoors", category="room_type")
