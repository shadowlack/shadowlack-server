import random
import re
import string

from server.conf import settings

from evennia.utils import evtable, evform, fill, dedent
from evennia.utils.evmenu import EvMenu, list_node, get_input

from world import races


def _help(caller):
    """
    """
    pass


def _calculate_height(caller):
    """
    Randomize a character's height based on race min and max height values.
    60% chance to be average height
    20% chance to be either short or tall
    """
    stature_deviation = ['short'] * 20 + ['tall'] * 20 + ['average'] * 60
    stature = random.choice(stature_deviation)
    if stature == "short":
        height_var = random.uniform(-0.05, -0.15)
    elif stature == "tall":
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

    race = races.load_race(chosen_race)

    # Default values
    caller.ndb._menutree.sheet = {}
    caller.ndb._menutree.sheet['name'] = None
    caller.ndb._menutree.sheet['race'] = race.name
    caller.ndb._menutree.sheet['weight'] = "Average"
    caller.ndb._menutree.sheet['age'] = 24

    caller.db.race = race
    _calculate_height(caller)

    return "choose_gender"


def menunode_race_and_bonuses(caller, raw_string):
    raw_string = raw_string.strip()
    if raw_string.isdigit() and int(raw_string) <= len(races.ALL_RACES):
        race = races.ALL_RACES[int(raw_string) - 1]
        race = races.load_race(race)
        caller.ndb._menutree.race = race

    race = caller.ndb._menutree.race

    text = race.desc
    options = [{"key": ("c", "continue"), "desc": "|gContinue|n character creation with {}.".format(
        race.plural_name), "goto": (_choose_race, {"race": race.name})}]

    options.append({"key": ("r", "_default"),
                    "desc": "Return to race selection.",
                    "goto": "choose_race"})

    return text, options


def choose_race(caller, raw_string, **kwargs):
    """
    Choose your character's race.
    """
    text = ("Choose your character's race. Select a race to learn more about them.", fill(
        "Your race determines some of your starting stats and bonus skills. Select a race to see more detailed information."))
    options = []

    for race in races.ALL_RACES:
        race = races.load_race(race)
        options.append({"desc": "{:<70.70s}...".format(race._desc),
                        "goto": "menunode_race_and_bonuses"})

    # Only admins may create Rapine
    """
    if caller.check_permstring("Admin"):
        options.append({"key": ("ra", "Rapine", "Rap"), "desc": "|404Rapine (Admin)|n", "goto": (
            menunode_race_and_bonuses, {"race": "Rapine"})})
    """
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
    options = [
        {"key": ("f"), "desc": "Female - she/her/hers",
         "goto": (_choose_gender, {"gender": "Female"})},
        {"key": ("m"), "desc": "Male - he/him/his",
         "goto": (_choose_gender, {"gender": "Male"})},
        {"key": ("n"), "desc": "Neutral - it/its/its",
         "goto": (_choose_gender, {"gender": "Neutral"})},
        {"key": ("a"), "desc": "Ambiguous - they/them/theirs", "goto": (_choose_gender, {"gender": "Ambiguous"})}]
    options.append({"key": ("r", "_default"),
                    "desc": "Return to race selection.", "goto": "choose_race"})

    return text, options


def _choose_weight(caller, raw_string, **kwargs):
    """
    Set your character's weight
    """
    weight = kwargs.get("weight", None)
    if not weight:
        caller.error_echo(
            "Something went wrong with weight selection.")
        return "choose_weight"
    caller.msg("|wYou set your weight to {}.|n".format(weight))
    caller.ndb._menutree.sheet['weight'] = weight
    return "look_at_me"


def choose_weight(caller, raw_string, **kwargs):
    """
    Choose your character's weight
    """
    text = "Choose your character's natural weight."
    options = []
    for weight in ["Underweight", "Light", "Average", "Heavy", "Obese"]:
        options.append({"key": (weight[:1].lower()), "desc": weight, "goto": (
            _choose_weight, {"weight": weight})})
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
    elif input_string == "weight":
        return "choose_weight"
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
    inp_age = raw_string.strip()

    if not inp_age.isdigit():
        caller.msg("|RInvalid age. You must enter a number.|n")
    else:
        inp_age = int(inp_age)
        if inp_age <= 0 or inp_age > 172:
            caller.msg(
                "|RInvalid age. You must enter a positive integer between 1 and 172.|n")
        else:
            caller.msg("|wYou set your age to {}.|n".format(inp_age))
            caller.ndb._menutree.sheet['age'] = inp_age
            caller.db.age = inp_age

    return "look_at_me"


def enter_age(caller, raw_string, **kwargs):
    text = ("How old is this character? (between 1 and 172)",
            "Your character's age must be between 1 and 172. Only positive integers are accepted.  Your character's age will determine certain rights and privileges in society, as well as closeness to death.")
    options = {"key": "_default",
               "goto": (_set_age, {})}
    return text, options


def _set_name(caller, raw_string, **kwargs):
    inp = raw_string.strip().capitalize()
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
    table.add_row("Weight", caller.ndb._menutree.sheet['weight'])
    table.reformat_column(0, align="r")

    options = (
        {"key": "name", "desc": "Name your character.", "goto": "enter_name"}, {"key": "age", "desc": "Change your character's age.", "goto": "enter_age"},  {"key": "height", "desc": "Not tall or short enough? Re-roll your character's height.", "goto": (_catch_default_input)}, {"key": "weight", "desc": "Adjust your character's weight (lighter, heavier, etc).", "goto": (_catch_default_input)}, {"key": ("c", "continue"), "desc": "|gContinue|n with character creation.", "goto": (_catch_default_input)}, {"key": "reset", "desc": "Reset your progress and start over character creation.", "goto": "choose_race"}, {"key": "_default", "goto": (_catch_default_input)})

    return table, options
