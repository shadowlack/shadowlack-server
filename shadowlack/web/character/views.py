# Views for our character app

from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView

from evennia.utils.search import object_search
from evennia.utils.utils import inherits_from

from evennia.web.website.views import CharacterListView, CharacterCreateView, CharacterManageView, CharacterUpdateView, CharacterDetailView, LoginRequiredMixin

from typeclasses.characters import Character
from web.character.forms import ShadowlackCharacterForm


def CharacterSheet(request, object_id):

    obj = get_object_or_404(Character, db_key=object_id)

    return render(request, 'character/character_sheet.html', {'object': obj})

class CharacterList(CharacterListView):
    """
    List all created characters
    """
    template_name = "character/character_list.html"


class CharacterCreate(CharacterCreateView):
    """
    Create a new character
    """
    template_name = "character/character_form.html"

    form_class = ShadowlackCharacterForm


class CharacterManage(CharacterManageView):
    """
    Let a player see their created characters
    """
    template_name = "character/character_manage_list.html"


class CharacterUpdate(CharacterUpdateView):
    """
    Update a character
    """
    template_name = "character/character_form.html"
