from evennia import Command


class CmdMsgColour(Command):
    """
    Turn off and on ANSI color parsing.

    Usage:
        |wmsgcolour|n on||off

    This turns ANSI-colours on/off.
    The default value is on.
    """

    key = "msgcolour"
    aliases = ["msgcolor", "setcolour", "setcolor"]
    locks = "cmd:all()"
    help_category = "Preferences"

    def func(self):
        """
        Implements the command.
        """
        self.args = self.args.strip()
        if not self.args or not self.args in ("on", "off"):
            self.caller.msg("Usage: setcolour on|off")
            return
        if self.args == "on":
            self.caller.db.msgcolour = True
            # send a message with a tiny bit of formatting, just for fun
            self.caller.msg("Message colour was turned |gon|n.")
        else:
            self.caller.db.msgcolour = False
            self.caller.msg("Message colour was turned off.")
