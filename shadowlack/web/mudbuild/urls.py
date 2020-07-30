# URL patterns for the character app

from django.conf.urls import url
from django.urls import path
from web.mudbuild.views import room_map

urlpatterns = [

    path("", room_map, name="room_map")
]
