import random
import re
import string

from server.conf import settings

from evennia.objects.models import ObjectDB
from evennia.server.sessionhandler import SESSIONS
from evennia.utils import evtable, evform, fill, dedent, utils, create, logger, search
from evennia.utils.evmenu import EvMenu, list_node, get_input

from world import races, skills


def menunode_start(caller, raw_string, **kwargs):
    """
    1. Choose your character's race.
    """
    caller.ndb._menutree.name = caller.new_char

    text = dedent("""
        |cWelcome to Shadowlack's character creation.|n

        To begin, please choose |m{}'s|n race. Choosing a race will bring up a race fact sheet. Type |yhelp|n at any time for more information.""").format(caller.ndb._menutree.name)
    help_text = fill(
        "Your race determines some of your starting stats and bonus skills.")
    options = []

    for race in races.ALL_RACES:
        race = races.load_race(race)
        options.append({"desc": "{:<70.70s}...".format(race._desc),
                        "goto": "menunode_display_race"})

    # Only admins may create Rapine
    """
    if caller.check_permstring("Admin"):
        options.append({"key": ("ra", "Rapine", "Rap"), "desc": "|404Rapine (Admin)|n", "goto": (
            menunode_display_race, {"race": "Rapine"})})
    """
    return (text, help_text), options


def menunode_display_race(caller, raw_string):
    """
    2. Display race selection. Has info about race and bonuses.
    """
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
                    "goto": "menunode_start"})

    return text, options


def _choose_race(caller, raw_string, **kwargs):
    """
    3. Confirm race selection
    """
    chosen_race = kwargs.get("race", None)

    if not chosen_race:
        caller.error_echo(
            "Something went wrong with race selection.")
        return "menunode_start"

    # default character here
    race = races.load_race(chosen_race)
    caller.db.race = race
    caller.ndb._menutree.race = race
    caller.ndb._menutree.age = 23
    caller.ndb._menutree.weight = "Average"

    # create skills
    caller.ndb._menutree.skill_choices = skills.ALL_SKILLS
    caller.ndb._menutree.skills = {}
    for skill in caller.ndb._menutree.skill_choices:
        caller.ndb._menutree.skills[skill] = 0

    caller.ndb._menutree.allocate = 0

    # generate a randomized height based upon selected race
    _calculate_height(caller)

    caller.msg(str(caller.ndb._menutree.skills))

    return "choose_gender"


def _choose_gender(caller, raw_string, **kwargs):
    gender = kwargs.get("gender", None)

    if not gender:
        caller.error_echo(
            "Something went wrong with gender selection.")
        return "choose_gender"

    caller.ndb._menutree.gender = gender

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
                    "desc": "Return to race selection.", "goto": "menunode_start"})

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
    caller.ndb._menutree.weight = weight
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
    if input_string == "age":
        return enter_age
    elif input_string == "weight":
        return "choose_weight"
    elif input_string == "height":
        """
        Re-roll a character's height
        """
        _calculate_height(caller)
        caller.msg("|wHeight re-rolled. You are now " +
                   caller.ndb._menutree.height_desc + " (" + caller.ndb._menutree.height + " metres). Heights for " + caller.db.race.plural_name + " average between " + str(caller.db.race.min_height) + " metres and " + str(caller.db.race.max_height) + " metres.|n")
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
            caller.ndb._menutree.age = inp_age

    return "look_at_me"


def enter_age(caller, raw_string, **kwargs):
    text = ("How old is this character? (between 1 and 172)",
            "Your character's age must be between 1 and 172. Only positive integers are accepted.  Your character's age will determine certain rights and privileges in society, as well as closeness to death.")
    options = {"key": "_default",
               "goto": (_set_age, {})}
    return text, options


def look_at_me(caller):

    # form = evform.EvForm("world/character_sheet.py")

    table = evtable.EvTable(border="incols")
    table.add_row("Name", caller.ndb._menutree.name)
    table.add_row("Race", caller.ndb._menutree.race.name)
    table.add_row("Age", caller.ndb._menutree.age)
    table.add_row("Gender", caller.ndb._menutree.gender)
    table.add_row("Height", caller.ndb._menutree.height +
                  " metres (" + caller.ndb._menutree.height_desc + ")")
    table.add_row("Weight", caller.ndb._menutree.weight)
    table.reformat_column(0, align="r")

    options = (
        {"key": "skills", "desc": "Allocate skills.", "goto": "allocate_skills"}, {"key": "age", "desc": "Change your character's age.", "goto": "enter_age"},  {"key": "height", "desc": "Not tall or short enough? Re-roll your character's height.", "goto": (_catch_default_input)}, {"key": "weight", "desc": "Adjust your character's weight (lighter, heavier, etc).", "goto": (_catch_default_input)}, {"key": ("c", "continue"), "desc": "|gContinue|n with character creation.", "goto": (_catch_default_input)}, {"key": "reset", "desc": "Reset your progress and start over character creation.", "goto": "menunode_start"}, {"key": "_default", "goto": (_catch_default_input)})

    return table, options


def allocate_skills(caller, raw_string, **kwargs):

    if caller.ndb._menutree.allocate == 0:
        text = "Choose a skill |m{}|n is |ggreat|n at. This will be considered their top talent.".format(
            caller.ndb._menutree.name)
    elif caller.ndb._menutree.allocate >= 1 and caller.ndb._menutree.allocate <= 2:
        text = "Choose a skill |m{}|n is |ggood|n at.".format(
            caller.ndb._menutree.name)
    elif caller.ndb._menutree.allocate >= 3 and caller.ndb._menutree.allocate <= 5:
        text = "Choose a skill |m{}|n is |gfair|n at.".format(
            caller.ndb._menutree.name)
    elif caller.ndb._menutree.allocate >= 6 and caller.ndb._menutree.allocate <= 9:
        text = "Choose a skill |m{}|n is |gaverage|n at.".format(
            caller.ndb._menutree.name)
    else:
        text = "You shall not pass."
        pass

    text += (" |w{}/10 points spent.|n").format(caller.ndb._menutree.allocate)

    help_text = (
        "Your skills form a pyramid. You start with one great skill, two good skills, three fair skills, and four average skills. Your race bonuses are applied on top of your base skills.")

    options = []

    for skill in caller.ndb._menutree.skill_choices:

        # Add indicator for existing race bonus
        bonus_text = ''
        if skill in caller.ndb._menutree.race.bonuses:
            bonus_text += " |g**race bonus**|n "

        # Load skill data
        skill = skills.load_skill(skill)
        skill_types = ''

        # Add indicator for if this skill can be used to attack and/or defend
        if skill.attack or skill.defend:
            skill_types += ' ('
            if skill.attack:
                skill_types += "|m+Attack|n"
            if skill.attack and skill.defend:
                skill_types += ' and '
            if skill.defend:
                skill_types += "|c+Defend|n"
            skill_types += ')'

        options.append({"desc": "|y{}|n. {}{}{}".format(
            skill.name, bonus_text, skill.desc, skill_types), "goto": (_allocate_skills, {"skill": skill.name})})

    return (text, help_text), options


def _allocate_skills(caller, raw_string, **kwargs):

    chosen_skill = kwargs.get("skill", None).lower()
    """
    Skill point pyramid
    ----
    4
    3 3
    2 2 2
    1 1 1 1
    ----
    1 great skills (+4)
    2 good skills (+3)
    3 fair skills (+2)
    4 average skills (+1)
    """

    point_assignment = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

    # Apply skill
    caller.ndb._menutree.skills[chosen_skill] = point_assignment[caller.ndb._menutree.allocate]
    caller.msg("|w{} skill has been successfully allocated.|n".format(
        chosen_skill.capitalize()))

    # Remove skill from future selections
    caller.ndb._menutree.skill_choices.remove(chosen_skill)
    caller.ndb._menutree.allocate += 1

    caller.msg(str(caller.ndb._menutree.skills))

    if caller.ndb._menutree.allocate == len(point_assignment):
        caller.msg("|wAll skill points have been spent.|n")
        return "look_at_me"

    return "allocate_skills"


def create_character():

    account = self.account

    # create the character
    start_location = ObjectDB.objects.get_id(settings.START_LOCATION)
    default_home = ObjectDB.objects.get_id(settings.DEFAULT_HOME)
    permissions = settings.PERMISSION_ACCOUNT_DEFAULT
    new_character = create.create_object(
        typeclass, key=key, location=start_location, home=default_home, permissions=permissions
    )
    # only allow creator (and developers) to puppet this char
    new_character.locks.add(
        "puppet:id(%i) or pid(%i) or perm(Developer) or pperm(Developer);delete:id(%i) or perm(Admin)"
        % (new_character.id, account.id, account.id)
    )
    account.db._playable_characters.append(new_character)


def menunode_end(caller, raw_string):
    """Character created."""
    caller.new_char.db.chargen_complete = True
    text = dedent("""
        You have completed Shadowlack character creation.""")
    return text, None


# Helpers


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

    caller.ndb._menutree.height = format(height, ".2f")
    caller.ndb._menutree.height_desc = caller.db.race.height_description(
        height)
    pass
