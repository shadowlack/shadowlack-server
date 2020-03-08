import random
import string

from server.conf import settings

from evennia.utils import evtable, evform
from evennia.utils.evmenu import EvMenu, list_node, get_input

from typeclasses.races import Anubi, Aquabat, Feydragon, Khell, Lukuo, Pendragon, Rapine, Takula, Yki


def _calculate_height(caller):
    """
    Randomize a character's height based on race min and max height values.
    60% chance to be average height
    20% chance to be either short or tall
    """
    my_list = ['short'] * 20 + ['tall'] * 20 + ['average'] * 60
    variation = random.choice(my_list)
    if variation == "short":
        height_var = random.uniform(-0.05, -0.15)
    elif variation == "tall":
        height_var = random.uniform(0.05, 0.15)
    else:
        height_var = 0.00

    height = random.uniform(caller.db.race.min_height,
                            caller.db.race.max_height)
    height = height + height_var

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

    # Default values
    caller.ndb._menutree.sheet = {}
    caller.ndb._menutree.sheet['name'] = None
    caller.ndb._menutree.sheet['race'] = race.name
    caller.ndb._menutree.sheet['build'] = "Average"
    caller.ndb._menutree.sheet['age'] = 24

    caller.db.race = race
    _calculate_height(caller)

    return "choose_gender"


def choose_race(caller, raw_string, **kwargs):
    """
    Choose your character's race.
    """
    text = ("Choose your character's race.",
            "Your race determines some of your starting stats and bonus skills.")
    options = []

    for race in ["Anubi", "Aquabat", "Feydragon", "Khell", "Lukuo", "Pendragon", "Takula", "Yki"]:
        options.append({"key": (race[:2].lower(), race), "desc": race, "goto": (
            _choose_race, {"race": race})})

    # Only admins may create Rapine
    if caller.check_permstring("Admin"):
        options.append({"key": ("ra", "Rapine", "Rap"), "desc": "|404Rapine (Admin)|n", "goto": (
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
        {"key": ("f"), "desc": "Female - she/her/hers",
         "goto": (_choose_gender, {"gender": "Female"})},
        {"key": ("m"), "desc": "Male - he/him/his",
         "goto": (_choose_gender, {"gender": "Male"})},
        {"key": ("n"), "desc": "Neutral - it/its/its",
         "goto": (_choose_gender, {"gender": "Neutral"})},
        {"key": ("a"), "desc": "Ambiguous - they/them/theirs", "goto": (_choose_gender, {"gender": "Ambiguous"})})

    return text, options


def _choose_build(caller, raw_string, **kwargs):
    """
    Set your character's build
    """
    build = kwargs.get("build", None)
    if not build:
        caller.error_echo(
            "Something went wrong with build selection.")
        return "choose_build"
    caller.msg("|wYou set your build to {}.|n".format(build))
    caller.ndb._menutree.sheet['build'] = build
    return "look_at_me"


def choose_build(caller, raw_string, **kwargs):
    """
    Choose your character's build
    """
    text = "Choose your character's natural build."
    options = []
    for build in ["Underweight", "Slight", "Average", "Heavy", "Obese"]:
        options.append({"key": (build[:1].lower()), "desc": build, "goto": (
            _choose_build, {"build": build})})
    return text, options


"""
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
"""


def _catch_default_input(caller, raw_string, **kwargs):
    input_string = raw_string.lower()
    caller.msg(input_string)
    if input_string == "name":
        return enter_name
    elif input_string == "age":
        return enter_age
    elif input_string == "build":
        return "choose_build"
    elif input_string == "height":
        """
        Re-roll a character's height
        """
        _calculate_height(caller)
        caller.msg("|wHeight re-rolled. You are now " +
                   caller.ndb._menutree.sheet['height_desc'] + " (" + caller.ndb._menutree.sheet['height'] + " metres). Heights for " + caller.db.race.plural_name + " average between " + str(caller.db.race.min_height) + " metres and " + str(caller.db.race.max_height) + " metres.|n")
        return "look_at_me"
    else:
        pass
    return "look_at_me"


def _set_age(caller, raw_string, **kwargs):
    inp = raw_string.strip()
    prev_age = kwargs.get("prev_age")
    caller.ndb._menutree.sheet['age'] = prev_age
    if not inp:
        if prev_age:
            caller.key = prev_age
            caller.msg("Your age was set to |w{}|n.".format(prev_age))
            return "look_at_me"
        else:
            caller.msg("Cancelled.")
            return "look_at_me"
    else:
        return None, {"prev_age": inp}


def enter_age(caller, raw_string, **kwargs):
    prev_age = kwargs.get("prev_age")
    if prev_age:
        text = "Change the age or |y<enter>|n to accept."
    else:
        text = "Enter your character's age or |y<enter>|n to cancel."
    options = {"key": "_default",
               "goto": (_set_age, {"prev_age": prev_age})}
    return text, options


def _set_name(caller, raw_string, **kwargs):
    inp = raw_string.strip()
    prev_name = kwargs.get("prev_name")
    caller.ndb._menutree.sheet['name'] = prev_name
    if not inp:
        if prev_name:
            caller.key = prev_name
            caller.msg("Your name was set to |w{}|n.".format(prev_name))
            return "look_at_me"
        else:
            caller.msg("Cancelled.")
            return "look_at_me"
    else:
        return None, {"prev_name": inp}


def enter_name(caller, raw_string, **kwargs):
    # check if we already entered a name before
    prev_name = kwargs.get("prev_name")
    if prev_name:
        text = "Change this name or |y<enter>|n to accept."
    else:
        text = "Enter your character's name or |y<enter>|n to cancel."
    options = {"key": "_default",
               "goto": (_set_name, {"prev_name": prev_name})}
    return text, options


def look_at_me(caller):

    # form = evform.EvForm("world/character_sheet.py")

    table = evtable.EvTable(border="incols")
    table.add_row("Name", caller.ndb._menutree.sheet['name'])
    table.add_row("Race", caller.ndb._menutree.sheet['race'])
    table.add_row("Age", caller.ndb._menutree.sheet['age'])
    table.add_row("Gender", caller.ndb._menutree.sheet['gender'])
    table.add_row("Height", caller.ndb._menutree.sheet['height'] +
                  " metres (" + caller.ndb._menutree.sheet['height_desc'] + ")")
    table.add_row("Build", caller.ndb._menutree.sheet['build'])
    table.reformat_column(0, align="r")

    options = (
        {"key": "name", "desc": "Name your character.", "goto": "enter_name"}, {"key": "age", "desc": "Change your character's age.", "goto": "enter_age"},  {"key": "height", "desc": "Not tall or short enough? Re-roll your character's height.", "goto": (_catch_default_input)}, {"key": "build", "desc": "Adjust your character's natural build (thinner, heavier, etc).", "goto": (_catch_default_input)}, {"key": "continue", "desc": "|yContinue|n with character creation.", "goto": (_catch_default_input)}, {"key": "reset", "desc": "Reset your progress and start over character creation.", "goto": "choose_race"}, {"key": "_default", "goto": (_catch_default_input)})

    return table, options
