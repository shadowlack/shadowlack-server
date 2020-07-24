import re
from re import escape as re_escape
import itertools

from django.conf import settings

from evennia import Command, CmdSet
from evennia.utils import logger
from evennia.commands.default.muxcommand import MuxCommand

from commands.roleplay import RPCommand

def _refresh_inventory_pane(self):
    """
    Refresh a character's user inventory pane.
    """
    items = self.caller.contents
    if not items:
        string = "You are not carrying anything."
        self.caller.msg((f"{string}", {"type": "inventory"}))
    else:
        table = self.styled_table(border="header")
        for item in items:
            table.add_row("|C%s|n" % item.name, item.db.desc or "")
        string = "|wYou are carrying:\n%s" % table
        self.caller.msg((f"{table}", {"type": "inventory"}))


class CmdInventory(RPCommand):
    """
    View inventory
    Usage:
      inventory
      inv
    Displays your inventory.
    """
    key = "inventory"
    aliases = ["inv", "i"]
    locks = "cmd:all()"
    help_category = "In Character"

    def func(self):
        """check inventory"""

        _refresh_inventory_pane(self)

        """
        items = self.caller.contents
        if not items:
            string = "You are not carrying anything."
            self.caller.msg((f"{string}", {"type": "inventory"}))
        else:
            table = self.styled_table(border="header")
            for item in items:
                table.add_row("|C%s|n" % item.name, item.db.desc or "")
            string = "|wYou are carrying:\n%s" % table
            # refresh inventory pane
            self.caller.msg((f"{table}", {"type": "inventory"}))
        self.caller.msg(string)
        """


class CmdGet(RPCommand):
    """
    pick up something
    Usage:
      get <obj>
    Picks up an object from your location and puts it in
    your inventory.
    """

    key = "get"
    aliases = "grab"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """implements the command."""

        caller = self.caller

        if not self.args:
            caller.msg("Get what?")
            return
        obj = caller.search(self.args, location=caller.location)
        if not obj:
            return
        if caller == obj:
            caller.msg("You can't get yourself.")
            return
        if not obj.access(caller, "get"):
            if obj.db.get_err_msg:
                caller.msg(obj.db.get_err_msg)
            else:
                caller.msg("You can't get that.")
            return

        # calling at_before_get hook method
        if not obj.at_before_get(caller):
            return

        obj.move_to(caller, quiet=True)
        caller.msg("You pick up %s." % obj.name)
        caller.location.msg_contents("%s picks up %s." % (
            caller.name, obj.name), exclude=caller)
        # calling at_get hook method
        obj.at_get(caller)


class CmdDrop(RPCommand):
    """
    drop something
    Usage:
      drop <obj>
    Lets you drop an object from your inventory into the
    location you are currently in.
    """

    key = "drop"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement command"""

        caller = self.caller
        if not self.args:
            caller.msg("Drop what?")
            return

        # Because the DROP command by definition looks for items
        # in inventory, call the search function using location = caller
        obj = caller.search(
            self.args,
            location=caller,
            nofound_string="You aren't carrying %s." % self.args,
            multimatch_string="You carry more than one %s:" % self.args,
        )
        if not obj:
            return

        # Call the object script's at_before_drop() method.
        if not obj.at_before_drop(caller):
            return

        obj.move_to(caller.location, quiet=True)
        caller.msg("You drop %s." % (obj.name,))
        caller.location.msg_contents("%s drops %s." % (
            caller.name, obj.name), exclude=caller)
        # Call the object script's at_drop() method.
        obj.at_drop(caller)


class CmdGive(RPCommand):
    """
    give away something to someone
    Usage:
      give <inventory obj> <to||=> <target>
    Gives an items from your inventory to another character,
    placing it in their inventory.
    """

    key = "give"
    rhs_split = ("=", " to ")  # Prefer = delimiter, but allow " to " usage.
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement give"""

        caller = self.caller
        if not self.args or not self.rhs:
            caller.msg("Usage: give <inventory object> = <target>")
            return
        to_give = caller.search(
            self.lhs,
            location=caller,
            nofound_string="You aren't carrying %s." % self.lhs,
            multimatch_string="You carry more than one %s:" % self.lhs,
        )
        target = caller.search(self.rhs)
        if not (to_give and target):
            return
        if target == caller:
            caller.msg("You keep %s to yourself." % to_give.key)
            return
        if not to_give.location == caller:
            caller.msg("You are not holding %s." % to_give.key)
            return

        # calling at_before_give hook method
        if not to_give.at_before_give(caller, target):
            return

        # give object
        caller.msg("You give %s to %s." % (to_give.key, target.key))
        to_give.move_to(target, quiet=True)
        target.msg("%s gives you %s." % (caller.key, to_give.key))
        # Call the object script's at_give() method.
        to_give.at_give(caller, target)


class ItemsCmdSet(CmdSet):
    """
    Mix-in for adding item-commands to default cmdset.
    """
    def at_cmdset_creation(self):
        self.add(CmdInventory())
        self.add(CmdGet())
        self.add(CmdDrop())
        self.add(CmdGive())

