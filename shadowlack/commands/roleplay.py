import re
from re import escape as re_escape
import itertools

from django.conf import settings

from evennia import Command, CmdSet
from evennia.utils import logger
from evennia.commands.default.muxcommand import MuxCommand

# ------------------------------------------------------------
# Emote parser
# ------------------------------------------------------------

# Settings

# The prefix is the (single-character) symbol used to find the start
# of a object reference, such as /tall (note that
# the system will understand multi-word references like '/a tall man' too).
_PREFIX = "/"

# The num_sep is the (single-character) symbol used to separate the
# sdesc from the number when  trying to separate identical sdescs from
# one another. This is the same syntax used in the rest of Evennia, so
# by default, multiple "tall" can be separated by entering 1-tall,
# 2-tall etc.
_NUM_SEP = "-"

# Texts

_EMOTE_NOMATCH_ERROR = """|RNo match for |r{ref}|R.|n"""

_EMOTE_MULTIMATCH_ERROR = """|RMultiple possibilities for {ref}:
    |r{reflist}|n"""

_RE_FLAGS = re.MULTILINE + re.IGNORECASE + re.UNICODE

_RE_PREFIX = re.compile(r"^%s" % _PREFIX, re.UNICODE)

# This regex will return groups (num, word), where num is an optional counter to
# separate multimatches from one another and word is the first word in the
# marker. So entering "/tall man" will return groups ("", "tall")
# and "/2-tall man" will return groups ("2", "tall").
_RE_OBJ_REF_START = re.compile(
    r"%s(?:([0-9]+)%s)*(\w+)" % (_PREFIX, _NUM_SEP), _RE_FLAGS)

_RE_LEFT_BRACKETS = re.compile(r"\{+", _RE_FLAGS)
_RE_RIGHT_BRACKETS = re.compile(r"\}+", _RE_FLAGS)
# Reference markers are used internally when distributing the emote to
# all that can see it. They are never seen by players and are on the form {#dbref}.
_RE_REF = re.compile(r"\{+\#([0-9]+)\}+")

# This regex is used to quickly reference one self in an emote.
_RE_SELF_REF = re.compile(r"/me|@", _RE_FLAGS)

# regex for non-alphanumberic end of a string
_RE_CHAREND = re.compile(r"\W+$", _RE_FLAGS)

# reference markers for language
_RE_REF_LANG = re.compile(r"\{+\##([0-9]+)\}+")
# language says in the emote are on the form "..." or langname"..." (no spaces).
# this regex returns in groups (langname, say), where langname can be empty.
_RE_LANGUAGE = re.compile(r"(?:\((\w+)\))*(\".+?\")")

# the emote parser works in two steps:
#  1) convert the incoming emote into an intermediary
#     form with all object references mapped to ids.
#  2) for every person seeing the emote, parse this
#     intermediary form into the one valid for that char.


class RPCommand(MuxCommand):
    locks = "cmd:all()"
    help_category = "In Character"

    def parse(self):
        "strip extra whitespace"
        self.args = self.args.strip()

class CmdEmote(RPCommand):  # replaces the main emote
    """
    Emote an action, allowing dynamic replacement of
    text in the emote.
    Usage:
      emote <message>
    Example:
      emote /me looks around.
      emote With a flurry /me attacks /tall man with his sword.
      emote "Hello", /me says.
    Describes an event in the world. This allows the use of /ref
    markers to replace with the short descriptions or recognized
    strings of objects in the same room. These will be translated to
    emotes to match each person seeing it. Use "..." for saying
    things and langcode"..." without spaces to say something in
    a different language.
    """

    key = "emote"
    aliases = [":", "em"]

    def func(self):
        "Perform the emote."
        if not self.args:
            self.caller.msg("What do you want to do?")
        else:
            # we also include ourselves here.
            emote = self.args
            targets = self.caller.location.contents
            if not emote.endswith((".", "?", "!")):  # If emote is not punctuated,
                emote = "%s." % emote  # add a full-stop for good measure.
            send_emote(self.caller, targets, emote, anonymous_add="first")


class CmdPose(RPCommand):  # set current pose and default pose
    """
    Set a static pose

    Usage:
        pose <pose>
        pose default <pose>
        pose reset
        pose obj = <pose>
        pose default obj = <pose>
        pose reset obj =

    Examples:
        pose leans against the tree
        pose is talking to the barkeep.
        pose box = is sitting on the floor.

    Set a static pose. This is the end of a full sentence that starts
    with your sdesc. If no full stop is given, it will be added
    automatically. The default pose is the pose you get when using
    pose reset. Note that you can use sdescs/recogs to reference
    people in your pose, but these always appear as that person's
    sdesc in the emote, regardless of who is seeing it.

    """

    key = "pose"

    def parse(self):
        """
        Extract the "default" alternative to the pose.
        """
        args = self.args.strip()
        default = args.startswith("default")
        reset = args.startswith("reset")
        if default:
            args = re.sub(r"^default", "", args)
        if reset:
            args = re.sub(r"^reset", "", args)
        target = None
        if "=" in args:
            target, args = [part.strip() for part in args.split("=", 1)]

        self.target = target
        self.reset = reset
        self.default = default
        self.args = args.strip()

    def func(self):
        "Create the pose"
        caller = self.caller
        pose = self.args
        target = self.target
        if not pose and not self.reset:
            caller.msg("Usage: pose <pose-text> OR pose obj = <pose-text>")
            return

        if not pose.endswith("."):
            pose = "%s." % pose
        if target:
            # affect something else
            target = caller.search(target)
            if not target:
                return
            if not target.access(caller, "edit"):
                caller.msg("You can't pose that.")
                return
        else:
            target = caller

        if not target.attributes.has("pose"):
            caller.msg("%s cannot be posed." % target.key)
            return

        target_name = target.sdesc.get() if hasattr(target, "sdesc") else target.key
        # set the pose
        if self.reset:
            pose = target.db.pose_default
            target.db.pose = pose
        elif self.default:
            target.db.pose_default = pose
            caller.msg("Default pose is now '%s %s'." % (target_name, pose))
            return
        else:
            # set the pose. We do one-time ref->sdesc mapping here.
            parsed, mapping = parse_sdescs_and_recogs(
                caller, caller.location.contents, pose)
            mapping = dict(
                (ref, obj.sdesc.get() if hasattr(obj, "sdesc") else obj.key)
                for ref, obj in mapping.items()
            )
            pose = parsed.format(**mapping)

            if len(target_name) + len(pose) > 60:
                caller.msg("Your pose '%s' is too long." % pose)
                return

            target.db.pose = pose

        caller.msg("Pose will read '%s %s'." % (target_name, pose))


class CmdSay(RPCommand):
    """
    Speak as your character.

    Usage:
      say <message>

    Talk to those in your current location.
    """

    key = "say"
    aliases = ['"', "'"]

    def func(self):
        "Run the say command"

        caller = self.caller

        if not self.args:
            caller.msg("Say what?")
            return

        # calling the speech modifying hook
        speech = caller.at_before_say(self.args)
        # preparing the speech with sdesc/speech parsing.
        targets = self.caller.location.contents
        send_emote(self.caller, targets, speech, anonymous_add=None)


class CmdSdesc(RPCommand):  # set/look at own sdesc
    """
    Assign yourself a short description (sdesc).

    Usage:
      sdesc <short description>

    Assigns a short description to yourself.

    """

    key = "sdesc"
    locks = "cmd:all()"

    def func(self):
        "Assign the sdesc"
        caller = self.caller
        if not self.args:
            caller.msg("Usage: sdesc <sdesc-text>")
            return
        else:
            # strip non-alfanum chars from end of sdesc
            sdesc = _RE_CHAREND.sub("", self.args)
            try:
                sdesc = caller.sdesc.add(sdesc)
            except SdescError as err:
                caller.msg(err)
                return
            except AttributeError:
                caller.msg(f"Cannot set sdesc on {caller.key}.")
                return
            caller.msg("%s's sdesc was set to '%s'." % (caller.key, sdesc))


class CmdRecog(RPCommand):  # assign personal alias to object in room
    """
    Recognize another character in the same room.

    Usage:
      recall
      recall <sdesc> as <alias>
      forget alias

    Example:
        recog a short teacher as Jaceen
        forget Jaceen

    This will assign a personal alias for a character, or forget said alias.
    Using the command without arguments will list all current recognitions.

    """

    key = "recog"
    aliases = ["recognize", "forget", "remember"]

    def parse(self):
        "Parse for the sdesc as alias structure"
        self.sdesc, self.alias = "", ""
        if " as " in self.args:
            self.sdesc, self.alias = [part.strip()
                                      for part in self.args.split(" as ", 2)]
        elif self.args:
            # try to split by space instead
            try:
                self.sdesc, self.alias = [part.strip()
                                          for part in self.args.split(None, 1)]
            except ValueError:
                self.sdesc, self.alias = self.args.strip(), ""

    def func(self):
        "Assign the recog"
        caller = self.caller
        alias = self.alias.rstrip(".?!")
        sdesc = self.sdesc

        recog_mode = self.cmdstring != "forget" and alias and sdesc
        forget_mode = self.cmdstring == "forget" and sdesc
        list_mode = not self.args

        if not (recog_mode or forget_mode or list_mode):
            caller.msg(
                "Usage: recog, recog <sdesc> as <alias> or forget <alias>")
            return

        if list_mode:
            # list all previously set recogs
            all_recogs = caller.recog.all()
            if not all_recogs:
                caller.msg(
                    "You recognize no-one. " "(Use 'recog <sdesc> as <alias>' to recognize characters."
                )
            else:
                # note that we don't skip those failing enable_recog lock here,
                # because that would actually reveal more than we want.
                lst = "\n".join(
                    " {}  ({})".format(key, obj.sdesc.get()
                                       if hasattr(obj, "sdesc") else obj.key)
                    for key, obj in all_recogs.items()
                )
                caller.msg(
                    f"Currently recognized (use 'recog <sdesc> as <alias>' to add "
                    f"new and 'forget <alias>' to remove):\n{lst}"
                )
            return

        prefixed_sdesc = sdesc if sdesc.startswith(
            _PREFIX) else _PREFIX + sdesc
        candidates = caller.location.contents
        matches = parse_sdescs_and_recogs(
            caller, candidates, prefixed_sdesc, search_mode=True)
        nmatches = len(matches)
        # handle 0 and >1 matches
        if nmatches == 0:
            caller.msg(_EMOTE_NOMATCH_ERROR.format(ref=sdesc))
        elif nmatches > 1:
            reflist = [
                "{}{}{} ({}{})".format(
                    inum + 1,
                    _NUM_SEP,
                    _RE_PREFIX.sub("", sdesc),
                    caller.recog.get(obj),
                    " (%s)" % caller.key if caller == obj else "",
                )
                for inum, obj in enumerate(matches)
            ]
            caller.msg(_EMOTE_MULTIMATCH_ERROR.format(
                ref=sdesc, reflist="\n    ".join(reflist)))

        else:
            # one single match
            obj = matches[0]
            if not obj.access(self.obj, "enable_recog", default=True):
                # don't apply recog if object doesn't allow it (e.g. by being masked).
                caller.msg("It's impossible to recognize them.")
                return
            if forget_mode:
                # remove existing recog
                caller.recog.remove(obj)
                caller.msg("%s will now know them only as '%s'." %
                           (caller.key, obj.recog.get(obj)))
            else:
                # set recog
                sdesc = obj.sdesc.get() if hasattr(obj, "sdesc") else obj.key
                try:
                    alias = caller.recog.add(obj, alias)
                except RecogError as err:
                    caller.msg(err)
                    return
                caller.msg("%s will now remember |w%s|n as |w%s|n." %
                           (caller.key, sdesc, alias))


class CmdMask(RPCommand):
    """
    Wear a mask

    Usage:
        mask <new sdesc>
        unmask

    This will put on a mask to hide your identity. When wearing
    a mask, your sdesc will be replaced by the sdesc you pick and
    people's recognitions of you will be disabled.

    """

    key = "mask"
    aliases = ["unmask"]

    def func(self):
        caller = self.caller
        if self.cmdstring == "mask":
            # wear a mask
            if not self.args:
                caller.msg("Usage: (un)mask sdesc")
                return
            if caller.db.unmasked_sdesc:
                caller.msg("You are already wearing a mask.")
                return
            sdesc = _RE_CHAREND.sub("", self.args)
            sdesc = "%s |H[masked]|n" % sdesc
            if len(sdesc) > 60:
                caller.msg("Your masked sdesc is too long.")
                return
            caller.db.unmasked_sdesc = caller.sdesc.get()
            caller.locks.add("enable_recog:false()")
            caller.sdesc.add(sdesc)
            caller.msg("You wear a mask as '%s'." % sdesc)
        else:
            # unmask
            old_sdesc = caller.db.unmasked_sdesc
            if not old_sdesc:
                caller.msg("You are not wearing a mask.")
                return
            del caller.db.unmasked_sdesc
            caller.locks.remove("enable_recog")
            caller.sdesc.add(old_sdesc)
            caller.msg("You remove your mask and are again '%s'." % old_sdesc)


class CmdWhisper(RPCommand):
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


class CmdYell(RPCommand):
    """
    Raise your voice and yell

    Usage:
      |wyell|n <message>

    Careful. Folks could overhear you.
    """
    key = "yell"
    aliases = "shout"

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


class CmdFeel(RPCommand):
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


class RPSystemCmdSet(CmdSet):
    """
    Mix-in for adding rp-commands to default cmdset.
    """

    def at_cmdset_creation(self):
        self.add(CmdEmote())
        self.add(CmdFeel())
        self.add(CmdSay())
        self.add(CmdSdesc())
        self.add(CmdPose())
        self.add(CmdRecog())
        self.add(CmdMask())
