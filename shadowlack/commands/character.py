import re
import string
from django.conf import settings

from evennia import CmdSet
from evennia.utils import logger, create, search
from evennia.utils.evmenu import EvMenu
from evennia.commands.command import Command
from evennia.commands.default.muxcommand import MuxCommand
from evennia.server.sessionhandler import SESSIONS

_MAX_NR_CHARACTERS = settings.MAX_NR_CHARACTERS
_MULTISESSION_MODE = settings.MULTISESSION_MODE


class CmdHatch(MuxCommand):
    """
    Create a new character. Please create using your character's first name. You will be able to add a last name (surname) later.

    Usage:
      hatch <charactername>
    Example:
      hatch Koani

    Begins the character creation process with your character's chosen name.
    """
    key = "hatch"
    locks = "cmd:pperm(Player)"
    help_category = "Character"

    account_caller = True

    def func(self):
        "Create the new character"
        account = self.account
        session = self.session
        if not self.args:
            self.msg("Usage: hatch <charactername>")
            return
        key = self.args.strip().capitalize()

        # No digits allowed in names
        if not key.isalpha():
            self.msg(
                "Character name must contain alphabetic (A-Z) characters only.")
            return

        charmax = _MAX_NR_CHARACTERS

        """
        if not account.is_superuser and (
            account.db._playable_characters and len(
                account.db._playable_characters) >= charmax
        ):
            self.msg("You may only create a maximum of %i characters." % charmax)
            return

        # Create the character
        from evennia.objects.models import ObjectDB

        start_location = ObjectDB.objects.get_id(settings.START_LOCATION)
        typeclass = settings.BASE_CHARACTER_TYPECLASS
        permissions = settings.PERMISSION_ACCOUNT_DEFAULT
        """

        new_character = key
        session.new_char = new_character

        EvMenu(session, "menus.character_create", startnode="menunode_start",
               cmdset_mergetype="Replace", cmd_on_exit="look", auto_quit=True, auto_look=True, auto_help=True)
        # cmd_on_exit=finish_char_callback


class CmdGender(MuxCommand):
    """
    Set your gender on yourself

    Usage:
      |wgender|n female||male||neutral||ambiguous

    This adds gender and associated pronouns to your character.
    The default value is Ambiguous.
    """

    key = "gender"
    aliases = "sex"
    locks = "cmd:all()"
    help_category = "Character"

    def func(self):
        """
        Implements the command.
        """
        caller = self.caller
        arg = self.args.strip().lower()
        if arg not in ("male", "female", "neutral", "ambiguous"):
            caller.msg("Usage: gender female||male||neutral||ambiguous")
            return
        caller.db.gender = arg
        caller.msg(f"Your gender was set to |g{arg.capitalize()}|n.")
