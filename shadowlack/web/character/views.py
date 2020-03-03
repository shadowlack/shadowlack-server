# Views for our character app

from django.http import Http404
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

from typeclasses.characters import Character

from evennia.utils.search import object_search
from evennia.utils.utils import inherits_from


def get_object(self, queryset=None):

    slug = slugify(self.kwargs.get("slug", ""))

    obj = next((x for x in queryset if slugify(x.db_key) == slug), None)

    # Check if this object was requested in a valid manner
    if not obj:
        raise HttpResponseBadRequest(
            "No %(verbose_name)s found matching the query"
            % {"verbose_name": queryset.model._meta.verbose_name}
        )

    return obj


def sheet(request, object_id):

    try:
        character = Character.objects.filter(db_key=object_id)
        obj = character[0]

    except IndexError:
        raise Http404("I couldn't find a character with that ID.")
    if not inherits_from(obj, settings.BASE_CHARACTER_TYPECLASS):
        raise Http404("I couldn't find a character with that ID. "
                      "Found something else instead.")
    return render(request, 'character/sheet.html', {'object': obj})
