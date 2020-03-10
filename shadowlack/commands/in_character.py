from evennia.utils import logger
from evennia.commands.default.muxcommand import MuxCommand


class CmdPose(MuxCommand):
    """
    Strike a pose.

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
    aliases = [":", "emote", "me", "em"]
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
        super().parse()
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


class CmdSay(MuxCommand):
    """
    Speak as your character
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
            caller.msg("Usage: say <message>")
            return

        speech = self.args

        # Calling the at_before_say hook on the character
        speech = caller.at_before_say(speech)

        # If speech is empty, stop here
        if not speech:
            return

        # Call the at_after_say hook on the character
        caller.at_say(speech, msg_self=True)


class CmdWhisper(MuxCommand):
    """
    Speak privately as your character to another
    Usage:
      whisper <character> = <message>
      whisper <char1>, <char2> = <message>
    Talk privately to one or more characters in your current location, without
    others in the room being informed.
    """

    key = "whisper"
    aliases = ['tell', "msg"]
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


class CmdYell(MuxCommand):
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


class CmdDream(MuxCommand):
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


class CmdFeel(MuxCommand):
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


class CmdEmit(MuxCommand):
    """
    @emit
    Usage:
      @emit[/switches] [<obj>, <obj>, ... =] <message>
      @remit           [<obj>, <obj>, ... =] <message>
      @pemit           [<obj>, <obj>, ... =] <message>
    Switches:
      room : limit emits to rooms only (default)
      players : limit emits to players only
      contents : send to the contents of matched objects too
    Emits a message to the selected objects or to
    your immediate surroundings. If the object is a room,
    send to its contents. @remit and @pemit are just
    limited forms of @emit, for sending to rooms and
    to players respectively.
    """
    key = "@emit"
    aliases = ["@pemit", "@remit", "\\\\"]
    locks = "cmd:all()"
    help_category = "Social"
    perm_for_switches = "Builders"
    arg_regex = None

    def get_help(self, caller, cmdset):
        """Returns custom help file based on caller"""
        if caller.check_permstring(self.perm_for_switches):
            return self.__doc__
        help_string = """
        @emit
        Usage :
            @emit <message>
        Emits a message to your immediate surroundings. This command is
        used to provide more flexibility than the structure of poses, but
        please remember to indicate your character's name.
        """
        return help_string

    def func(self):
        """Implement the command"""

        caller = self.caller
        if caller.check_permstring(self.perm_for_switches):
            args = self.args
        else:
            args = self.raw.lstrip(" ")

        if not args:
            string = "Usage: "
            string += "\n@emit[/switches] [<obj>, <obj>, ... =] <message>"
            string += "\n@remit           [<obj>, <obj>, ... =] <message>"
            string += "\n@pemit           [<obj>, <obj>, ... =] <message>"
            caller.msg(string)
            return

        rooms_only = 'rooms' in self.switches
        players_only = 'players' in self.switches
        send_to_contents = 'contents' in self.switches
        perm = self.perm_for_switches
        normal_emit = False

        # we check which command was used to force the switches
        if (self.cmdstring == '@remit' or self.cmdstring == '@pemit') and not caller.check_permstring(perm):
            caller.msg("Those options are restricted to GMs only.")
            return
        self.caller.posecount += 1
        if self.cmdstring == '@remit':
            rooms_only = True
            send_to_contents = True
        elif self.cmdstring == '@pemit':
            players_only = True

        if not caller.check_permstring(perm):
            rooms_only = False
            players_only = False

        if not self.rhs or not caller.check_permstring(perm):
            message = args
            normal_emit = True
            objnames = []
            do_global = False
        else:
            do_global = True
            message = self.rhs
            if caller.check_permstring(perm):
                objnames = self.lhslist
            else:
                objnames = [
                    x.key for x in caller.location.contents if x.player]
        if do_global:
            do_global = caller.check_permstring(perm)
        # normal emits by players are just sent to the room
        if normal_emit:
            gms = [
                ob for ob in caller.location.contents if ob.check_permstring('builders')]
            non_gms = [
                ob for ob in caller.location.contents if "emit_label" in ob.tags.all() and ob.player]
            gm_msg = "{w[{c%s{w]{n %s" % (caller.name, message)
            caller.location.msg_contents(gm_msg, from_obj=caller, options={
                                         'is_pose': True}, gm_msg=True)
            for ob in non_gms:
                ob.msg(gm_msg, from_obj=caller, options={'is_pose': True})
            caller.location.msg_contents(
                message, exclude=gms + non_gms, from_obj=caller, options={'is_pose': True})
            return
        # send to all objects
        for objname in objnames:
            if players_only:
                obj = caller.player.search(objname)
                if obj:
                    obj = obj.character
            else:
                obj = caller.search(objname, global_search=do_global)
            if not obj:
                caller.msg("Could not find %s." % objname)
                continue
            if rooms_only and obj.location:
                caller.msg("%s is not a room. Ignored." % objname)
                continue
            if players_only and not obj.player:
                caller.msg("%s has no active player. Ignored." % objname)
                continue
            if obj.access(caller, 'tell'):
                if obj.check_permstring(perm):
                    bmessage = "{w[Emit by: {c%s{w]{n %s" % (
                        caller.name, message)
                    obj.msg(bmessage, options={'is_pose': True})
                else:
                    obj.msg(message, options={'is_pose': True})
                if send_to_contents and hasattr(obj, "msg_contents"):
                    obj.msg_contents(message, from_obj=caller, kwargs={
                                     'options': {'is_pose': True}})
                    caller.msg("Emitted to %s and contents:\n%s" %
                               (objname, message))
                elif caller.check_permstring(perm):
                    caller.msg("Emitted to %s:\n%s" % (objname, message))
            else:
                caller.msg("You are not allowed to emit to %s." % objname)
