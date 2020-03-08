import random
import string

from server.conf import settings

from evennia.utils import evtable, evform
from evennia.utils.evmenu import EvMenu, list_node, get_input

from typeclasses.races import Anubi, Aquabat, Feydragon, Khell, Lukuo, Pendragon, Takula, Yki


def _calculate_height(caller):
    """
    Randomize a character's height based on race min and max height values.
    """

    # 60% chance to be average height
    # 20% chance to be either short or tall
    my_list = ['short'] * 20 + ['tall'] * 20 + ['average'] * 60
    variation = random.choice(my_list)
    if variation == "short":
        height_var = random.uniform(-0.05, -0.15)
    elif variation == "tall":
        height_var = random.uniform(0.05, 0.15)
    else:
        height_var = 0.00

    caller.msg(height_var)
    caller.msg(caller.db.race.min_height)
    caller.msg(caller.db.race.max_height)
    height = random.uniform(caller.db.race.min_height,
                            caller.db.race.max_height)
    height = height + height_var

    caller.msg(height)
    caller.db.height = height
    caller.ndb._menutree.sheet['height'] = format(height, ".2f")
    caller.ndb._menutree.sheet['height_desc'] = caller.db.race.height_description(
        height)
    pass


def _choose_race(caller, raw_string, **kwargs):

    chosen_race = kwargs.get("race", None)

    if not chosen_race:
        caller.error_echo(
            "Something went wrong with race selection.")
        return "choose_race"

    if chosen_race == "Anubi":
        race = Anubi()
    elif chosen_race == "Aquabat":
        race = Aquabat()
    elif chosen_race == "Feydragon":
        race = Feydragon()
    elif chosen_race == "Khell":
        race = Khell()
    elif chosen_race == "Lukuo":
        race = Lukuo()
    elif chosen_race == "Pendragon":
        race = Pendragon()
    elif chosen_race == "Takula":
        race = Takula()
    elif chosen_race == "Yki":
        race = Yki()
    elif chosen_race == "Rapine":
        race = Rapine()
    else:
        return "choose_race"

    caller.ndb._menutree.sheet = {}
    caller.ndb._menutree.sheet['name'] = None
    caller.ndb._menutree.sheet['race'] = race.name

    # determine height and weight
    caller.db.race = race
    _calculate_height(caller)

    """
    height = random.uniform(race.min_height, race.max_height)
    caller.db.height = height

    caller.ndb._menutree.sheet['height'] = format(height, ".2f")
    caller.ndb._menutree.sheet['height_desc'] = race.height_description(
        height)
    """

    #
    # self.db.race.height_description(self.db.height)

    return "choose_gender"


def choose_race(caller, raw_string, **kwargs):
    """
    Choose your character's race.
    """
    text = "Choose your character's race."
    options = []

    for race in ["Anubi", "Aquabat", "Feydragon", "Khell", "Lukuo", "Pendragon", "Takula", "Yki"]:
        options.append({"desc": race, "goto": (
            _choose_race, {"race": race})})

    # Only admins may create Rapine
    if caller.check_permstring("Admin"):
        options.append({"desc": "|404Rapine (Admin)|n", "goto": (
            _choose_race, {"race": "Rapine"})})

    return text, options


def _choose_gender(caller, raw_string, **kwargs):
    gender = kwargs.get("gender", None)

    if not gender:
        caller.error_echo(
            "Something went wrong with gender selection.")
        return "choose_gender"

    caller.ndb._menutree.sheet['gender'] = gender

    return "look_at_me"


def choose_gender(caller):
    text = "Choose your character's gender. This will affect what pronouns are used to refer to them."
    options = (
        {"desc": "Female - she/her/hers",
         "goto": (_choose_gender, {"gender": "Female"})},
        {"desc": "Male - he/him/his",
         "goto": (_choose_gender, {"gender": "Male"})},
        {"desc": "Neutral - it/its/its",
         "goto": (_choose_gender, {"gender": "Neutral"})},
        {"desc": "Ambiguous - they/them/theirs", "goto": (_choose_gender, {"gender": "Ambiguous"})})

    return text, options


def choose_how_babby_formed(caller):
    text = "Can your character become pregnant?"
    options = ({"key": ("1", "y", "yes"), "desc": "Yes"},
               {"key": ("2", "n", "N"), "desc": "No"})
    return text, options


def choose_how_babby_formed(caller):
    text = "Can your character make others pregnant?"
    options = ({"key": ("1", "y", "yes"), "desc": "Yes"},
               {"key": ("2", "n", "N"), "desc": "No"})
    return text, options


def _catch_default_input(caller, raw_string, **kwargs):
    input_string = raw_string.lower()
    caller.msg(input_string)
    if input_string == "name":
        return enter_name
    elif input_string == "age":
        return enter_age
    elif input_string == "height":
        """
        Re-roll a character's height
        """
        _calculate_height(caller)
        caller.msg("Height rerolled. You are now " +
                   caller.ndb._menutree.sheet['height_desc'])
        return "look_at_me"
    else:
        pass
    return "look_at_me"


def _set_name(caller, raw_string, **kwargs):

    inp = raw_string.strip()

    prev_entry = kwargs.get("prev_entry")
    caller.ndb._menutree.sheet['name'] = prev_entry

    caller.msg(inp)

    if not inp:
        # a blank input either means OK or Abort
        if prev_entry:
            # Name
            caller.key = prev_entry
            caller.msg("Set name to {}.".format(prev_entry))
            return "look_at_me"
        else:
            caller.msg("Cancelled.")
            return "look_at_me"
    else:
        # re-run old node, but pass in the name given
        return None, {"prev_entry": inp}


def enter_name(caller, raw_string, **kwargs):

    # check if we already entered a name before
    prev_entry = kwargs.get("prev_entry")

    if prev_entry:
        text = "Change this name or <return> to accept."
    else:
        text = "Enter your character's name or <return> to cancel."

    options = {"key": "_default",
               "goto": (_set_name, {"prev_entry": prev_entry})}

    return text, options


def look_at_me(caller):

    form = evform.EvForm("world/character_sheet.py")

    table = evtable.EvTable(border="incols")
    table.add_row("race", caller.ndb._menutree.sheet['race'])
    table.add_row("gender", caller.ndb._menutree.sheet['gender'])
    table.add_row("height", caller.ndb._menutree.sheet['height'] +
                  " metres (" + caller.ndb._menutree.sheet['height_desc'] + ")")

    form.map(cells={1: "Tom the Bouncer",
                    2: "Griatch",
                    3: caller.ndb._menutree.sheet['name'],
                    4: 12,
                    5: 10,
                    6:  5,
                    7: 18,
                    8: 10,
                    9:  3})
    # add the tables to the proper ids in the form
    form.map(tables={"B": table})

    options = ({"key": "name", "desc": "name your character", "goto": "enter_name"}, {"key": "height", "desc": "Not tall or short enough? Re-roll your character's height.", "goto": (_catch_default_input)}, {
               "key": "reset", "desc": "Type reset to restart character creation.", "goto": "choose_race"}, {"key": "_default", "goto": (_catch_default_input)})

    return form, options
