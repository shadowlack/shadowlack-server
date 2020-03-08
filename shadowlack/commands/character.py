from evennia.utils import logger
from evennia.utils import logger, create, search
from evennia.utils.evmenu import EvMenu
from evennia.commands.default.muxcommand import MuxCommand


class CmdNew(MuxCommand):
    """
    Create a new character

    Usage:
      new
    """
    key = "new"
    locks = "cmd:all()"
    help_category = "Character"

    def func(self):

        EvMenu(self.caller, "menus.character_create", startnode="choose_race",
               cmdset_mergetype="Replace", cmd_on_exit="look", auto_quit=True, auto_look=True, auto_help=True)


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
        caller.db.gender = arg.capitalize()
        caller.msg("Your gender was set to |g%s|n." % caller.db.gender)
