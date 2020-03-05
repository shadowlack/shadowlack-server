from evennia.utils import logger

from commands.command import Command
from evennia.commands.default.general import CmdPose, CmdSay, CmdWhisper


class CmdPose(CmdPose):
    __doc__ = CmdPose.__doc__
    """
    strike a pose
    Usage:
      pose <pose text>
      pose's <pose text>
    Example:
      pose is standing by the wall, smiling.
       -> others will see:
      Tom is standing by the wall, smiling.
    Describe an action being taken. The pose text will
    automatically begin with your name.
    """
    key = "pose"
    aliases = [":", "emote", "/me"]
    locks = "cmd:all()"
    help_category = "In Character"

    def parse(self):
        """
        Custom parse the cases where the emote
        starts with some special letter, such
        as 's, at which we don't want to separate
        the caller's name and the emote with a
        space.
        """
        args = self.args
        if args and not args[0] in ["'", ",", ":"]:
            args = " %s" % args.strip()
        self.args = args

    def func(self):
        """Hook function"""
        if not self.args:
            msg = "What do you want to do?"
            self.caller.msg(msg)
        else:
            msg = "%s%s" % (self.caller.name, self.args)
            self.caller.location.msg_contents(
                text=(msg, {"type": "pose"}), from_obj=self.caller)


class CmdSay(CmdSay):
    """
    speak as your character
    Usage:
      say <message>
    Talk to those in your current location.
    """

    key = "say"
    aliases = ['"', "'"]
    locks = "cmd:all()"
    help_category = "In Character"

    def func(self):
        """Run the say command"""

        caller = self.caller

        if not self.args:
            caller.msg("Say what?")
            return

        speech = self.args

        # Calling the at_before_say hook on the character
        speech = caller.at_before_say(speech)

        # If speech is empty, stop here
        if not speech:
            return

        # Call the at_after_say hook on the character
        caller.at_say(speech, msg_self=True)


class CmdWhisper(CmdWhisper):
    """
    Speak privately as your character to another
    Usage:
      whisper <character> = <message>
      whisper <char1>, <char2> = <message>
    Talk privately to one or more characters in your current location, without
    others in the room being informed.
    """

    key = "whisper"
    aliases = ['tell', "/msg"]
    locks = "cmd:all()"
    help_category = "In Character"

    def func(self):
        """Run the whisper command"""

        caller = self.caller

        if not self.lhs or not self.rhs:
            caller.msg("Usage: whisper <character> = <message>")
            return

        receivers = [recv.strip() for recv in self.lhs.split(",")]

        receivers = [caller.search(receiver) for receiver in set(receivers)]
        receivers = [recv for recv in receivers if recv]

        speech = self.rhs
        # If the speech is empty, abort the command
        if not speech or not receivers:
            return

        # Call a hook to change the speech before whispering
        speech = caller.at_before_say(
            speech, whisper=True, receivers=receivers)

        # no need for self-message if we are whispering to ourselves (for some reason)
        msg_self = None if caller in receivers else True
        caller.at_say(speech, msg_self=msg_self,
                      receivers=receivers, whisper=True)


class CmdYell(Command):
    """
    Raise your voice and yell

    Usage:
      |wyell|n <message>

    Careful. Folks could overhear you.
    """
    key = "yell"
    aliases = "shout"
    locks = "cmd:all()"
    help_category = "In Character"

    def func(self):
        """
        Implements the command.
        """
        speaker = self.caller
        arg = self.args.strip().upper()
        # what everyone sees
        msg = "%s yells, |r\"%s\"|n" % (speaker.name, arg)
        speaker.location.msg_contents(
            text=msg, from_obj=speaker)


class CmdDream(Command):
    """
    Dream a dream.

    Usage:
      |wdream|n <message>

    Can possibly be seen by other dreamers and strong telepaths.
    """
    key = "dream"
    locks = "cmd:all()"
    help_category = "In Character"

    def func(self):
        """
        Implements the command.
        """
        # @todo only if a telepath
        caller = self.caller
        caller.msg("You dream: %s" % self.args)


class CmdFeel(Command):
    """
    State what your character is feeling

    Usage:
      |wfeel|n <message>

    Can possibly be felt by strong telepaths.

    """
    key = "feel"
    locks = "cmd:all()"
    help_category = "In Character"

    def func(self):
        """
        Implements the command.
        """
        caller = self.caller
        caller.msg("You feel: %s" % self.args)
