from evennia.utils import logger

from commands.command import Command


class CmdGender(Command):
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
