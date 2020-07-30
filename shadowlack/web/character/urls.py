# URL patterns for the character app

from django.conf.urls import url
from django.urls import path
from web.character.views import CharacterList, CharacterCreate, CharacterManage, CharacterUpdate, CharacterSheet

from evennia.web.website import views as website_views

urlpatterns = [
    # url(r'^/sheet/(?P<object_id>\d+)/$', sheet, name="sheet")

    url(
        r'^~(?P<object_id>\w+)/$',
        CharacterSheet,
        name="sheet"
    ),
    # /characters/ - list
    url(
        r"^characters/$",
        CharacterList.as_view(),
        name="characters"
    ),
    url(
        r"^characters/create/$",
        CharacterCreate.as_view(),
        name="character-create",
    ),
    url(
        r"^characters/manage/$",
        CharacterManage.as_view(),
        name="character-manage",
    ),
    url(
        r"^characters/update/(?P<slug>[\w\d\-]+)/(?P<pk>[0-9]+)/$",
        CharacterUpdate.as_view(),
        name="character-update",
    )
]
