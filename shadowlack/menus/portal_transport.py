import re
import string

from server.conf import settings

from evennia.objects.models import ObjectDB
from evennia.server.sessionhandler import SESSIONS
from evennia.utils import evtable, evform, fill, dedent, utils, create, logger, search
from evennia.utils.evmenu import EvMenu, list_node, get_input


def portal_start(caller, raw_string, **kwargs):
    text = "Where are you going today?"
    help_text = "This is a blurb about travel."
    options = []

    return (text, help_text), options
