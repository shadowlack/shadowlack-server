import random
import re
import string

from server.conf import settings

from evennia.objects.models import ObjectDB
from evennia.server.sessionhandler import SESSIONS
from evennia.utils import evtable, evform, fill, dedent, utils, create, logger, search
from evennia.utils.evmenu import EvMenu, list_node, get_input

from typeclasses import characters
from world import species, skills


def menunode_start(caller, raw_string, **kwargs):
    """
    1. Choose your character's species.
    """
    caller.ndb._menutree.name = caller.new_char
    caller.ndb._menutree.age = 23
    caller.ndb._menutree.species = None
    caller.ndb._menutree.weight = "average"
    caller.ndb._menutree.height = None
    caller.ndb._menutree.height_desc = None
    caller.ndb._menutree.gender = "ambiguous"
    caller.ndb._menutree.pronoun = "they"

    _character_pane(caller)

    caller.msg(("Shit's empty.", {
               "type": "inventory"}))

    text = dedent("""
        |cWelcome to Shadowlack's character creation.|n

        To begin, please choose |m{}'s|n species. Choosing a species will bring up a species fact sheet. Type |yhelp|n at any time for more information.""").format(caller.ndb._menutree.name)
    help_text = fill(
        "Your species determines some of your starting stats and bonus skills.")
    options = []

    for sp in species.ALL_SPECIES:
        sp = species.load_species(sp)
        options.append({"desc": "{:<70.70s}...".format(sp._desc),
                        "goto": "menunode_display_species"})

    # Only admins may create Rapine
    """
    if caller.check_permstring("Admin"):
        options.append({"key": ("ra", "Rapine", "Rap"), "desc": "|404Rapine (Admin)|n", "goto": (
            menunode_display_species, {"species": "Rapine"})})
    """
    return (text, help_text), options


def menunode_display_species(caller, raw_string):
    """
    2. Display species selection. Has info about species and bonuses.
    """
    raw_string = raw_string.strip()

    if raw_string.isdigit() and int(raw_string) <= len(species.ALL_SPECIES):
        char_species = species.ALL_SPECIES[int(raw_string) - 1]
        char_species = species.load_species(char_species)
        caller.ndb._menutree.species = char_species

    char_species = caller.ndb._menutree.species

    text = char_species.desc
    options = [{"key": ("c", "continue"), "desc": "|gContinue|n character creation with {}.".format(
        char_species.plural_name), "goto": (_choose_species, {"species": char_species.name})}]

    options.append({"key": ("r", "_default"),
                    "desc": "Return to species selection.",
                    "goto": "menunode_start"})

    return text, options


def _choose_species(caller, raw_string, **kwargs):
    """
    3. Confirm species selection
    """
    chosen_species = kwargs.get("species", None)

    if not chosen_species:
        caller.error_echo(
            "Something went wrong with species selection.")
        return "menunode_start"

    # default character here
    char_species = species.load_species(chosen_species)
    caller.db.species = char_species
    caller.ndb._menutree.species = char_species

    # generate a randomized height based upon selected species
    _calculate_height(caller)

    return "choose_gender"


def _choose_gender(caller, raw_string, **kwargs):
    gender = kwargs.get("gender", None)

    if not gender:
        caller.error_echo(
            "Something went wrong with pronoun selection.")
        return "choose_gender"

    caller.ndb._menutree.gender = gender
    caller.ndb._menutree.pronoun = characters.GENDER_PRONOUN_MAP[gender]['s']
    _character_pane(caller)

    return "look_at_me"


def choose_gender(caller):
    text = "Choose your character's pronouns. This will affect how your character is referenced."
    options = [
        {"key": ("f"), "desc": "she/her/hers",
         "goto": (_choose_gender, {"gender": "female"})},
        {"key": ("m"), "desc": "he/him/his",
         "goto": (_choose_gender, {"gender": "male"})},
        {"key": ("n"), "desc": "it/its/its",
         "goto": (_choose_gender, {"gender": "neutral"})},
        {"key": ("a"), "desc": "they/them/theirs", "goto": (_choose_gender, {"gender": "ambiguous"})}]
    options.append({"key": ("r", "_default"),
                    "desc": "Return to species selection.", "goto": "menunode_start"})

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
    _character_pane(caller)
    return "look_at_me"


def choose_weight(caller, raw_string, **kwargs):
    """
    Choose your character's weight
    """
    text = "Choose your character's natural weight."
    options = []
    for weight in ["underweight", "light", "average", "heavy", "obese"]:
        options.append({"key": (weight[:1].lower()), "desc": weight, "goto": (
            _choose_weight, {"weight": weight})})
    return text, options


def choose_anatomy(caller, raw_string, **kwargs):
    """
    Choose your character's anatomy/mutations
    """
    text = "Build the physical aspects of your character. Some anatomy aspects are dependent upon your character's species."
    options = []

    # height and weight
    options.append({"key": ("height"),
                    "desc": f"Not tall or short enough? Re-roll |m{caller.ndb._menutree.name}|n's height.", "goto": (_catch_default_input)})
    options.append({"key": ("weight"),
                    "desc": f"Adjust |m{caller.ndb._menutree.name}|n's weight (lighter, heavier, etc).", "goto": (_catch_default_input)})

    # _toggle_display(text, val, bool=True):
    # species
    # feydragon
    # lukuo
    # takula
    options.append({"key": ("horns"), "desc": _toggle_display(f"Does {caller.ndb._menutree.pronoun} have horns?", False, False), "goto": (_catch_default_input)})

    # reproduction
    options.append({"key": ("fertility"),
                    "desc": _toggle_display(f"Can {caller.ndb._menutree.pronoun} reproduce?", True, True), "goto": (_catch_default_input)})
    options.append({"key": ("pregnancy"),
                    "desc": _toggle_display(f"Can {caller.ndb._menutree.pronoun} become pregnant?", None, True), "goto": (_catch_default_input)})

    # menu defaults
    options.append({"key": ("r", "_default"), "desc": "Reset your progress and start over character creation.", "goto": "menunode_start"})
    options.append({"key": ("c", "continue"),
                    "desc": "|gContinue|n with character creation.", "goto": "look_at_me"})

    return text, options


"""
def choose_how_babby_formed(caller):
    text = "Can x become pregnant?"
    options = ({"key": ("1", "y", "yes"), "desc": "Yes"},
               {"key": ("2", "n", "N"), "desc": "No"})
    return text, options


def choose_can_babby_formed(caller):
    text = "Can x produce offspring? Are they fertile?"
    options = ({"key": ("1", "y", "yes"), "desc": "Yes"},
               {"key": ("2", "n", "N"), "desc": "No"})
    return text, options
"""


def _catch_default_input(caller, raw_string, **kwargs):
    input_string = raw_string.lower()
    if input_string == "age":
        return enter_age
    elif input_string == "is_fertile":
        pass
    elif input_string == "weight":
        return "choose_weight"
    elif input_string == "height":
        """
        Re-roll a character's height
        """
        _calculate_height(caller)
        _character_pane(caller)
        caller.msg("|wHeight re-rolled. You are now " +
                   caller.ndb._menutree.height_desc + " (" + caller.ndb._menutree.height + " metres). Heights for " + caller.db.species.plural_name + " average between " + str(caller.db.species.min_height) + " metres and " + str(caller.db.species.max_height) + " metres.|n")
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
            _character_pane(caller)

    return "look_at_me"


def enter_age(caller, raw_string, **kwargs):
    text = ("How old is this character? (between 1 and 172)",
            "Your character's age must be between 1 and 172. Only positive integers are accepted.  Your character's age will determine certain rights and privileges in society, as well as closeness to death.")
    options = {"key": "_default",
               "goto": (_set_age, {})}
    return text, options


def look_at_me(caller):

    # Create skills
    caller.ndb._menutree.allocate = 0
    caller.ndb._menutree.skill_choices = skills.ALL_SKILLS.copy()
    caller.ndb._menutree.skills = {}
    for skill in caller.ndb._menutree.skill_choices:
        caller.ndb._menutree.skills[skill] = 0

    table = evtable.EvTable(border="incols")
    table.add_row("Name", caller.ndb._menutree.name)
    table.add_row("Species", caller.ndb._menutree.species.name)
    table.add_row("Age", caller.ndb._menutree.age)
    table.add_row("Pronouns", caller.ndb._menutree.gender)
    table.add_row("Height", caller.ndb._menutree.height +
                  " metres (" + caller.ndb._menutree.height_desc + ")")
    table.add_row("Weight", caller.ndb._menutree.weight)
    table.reformat_column(0, align="r")

    options = (
        {"key": "anatomy", "desc": "Change your character's physical anatomy.",
            "goto": "choose_anatomy"},
        {"key": "age", "desc": "Change your character's age.", "goto": "enter_age"}, {"key": "r", "desc": "Reset your progress and start over character creation.", "goto": "menunode_start"}, {"key": ("c", "continue"), "desc": "|gContinue|n with character skill allocation.", "goto": "allocate_skills"}, {"key": "_default", "goto": (_catch_default_input)})

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
        "Your skills form a pyramid. You start with one great skill, two good skills, three fair skills, and four average skills. Your species bonuses are applied on top of your base skills.")

    options = []

    for skill in caller.ndb._menutree.skill_choices:

        # Add indicator for existing species bonus
        bonus_text = ''
        if skill in caller.ndb._menutree.species.bonuses:
            bonus_text += "|g**species bonus**|n "

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

    options.append({"key": ("r", "_default"),
                    "desc": "Reset skill point allocation.",
                    "goto": "look_at_me"})

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

    if caller.ndb._menutree.allocate == len(point_assignment):
        caller.msg("|wAll skill points have been spent.|n")
        return "character_sheet"

    return "allocate_skills"


def _character_pane(caller):
    form = evform.EvForm("world/character_pane.py")

    name_string = f"|m{caller.ndb._menutree.name}|n"

    if caller.ndb._menutree.species is None:
        name_string = f"|m{caller.ndb._menutree.name}|n"
    else:
        name_string = f"|m{caller.ndb._menutree.name}|n the {caller.ndb._menutree.height_desc} {caller.ndb._menutree.species.name}"

    #caller.ndb._menutree.gender
    form.map(cells={
        1: name_string,
        3: caller.ndb._menutree.age,
        4: f"{characters.GENDER_PRONOUN_MAP[caller.ndb._menutree.gender]['s']}/{characters.GENDER_PRONOUN_MAP[caller.ndb._menutree.gender]['o']}",
        5: caller.ndb._menutree.height,
        6: caller.ndb._menutree.weight
    })

    caller.msg((f"{form}", {"type": "character"}))

def character_sheet(caller, raw_string, **kwargs):
    options = []
    help_text = "This is your character sheet. Does everything look good to you?"

    form = evform.EvForm("world/character_sheet.py")

    name_string = "|m{}|n the {} {}".format(
        caller.ndb._menutree.name, caller.ndb._menutree.height_desc, caller.ndb._menutree.species.name)

    table_skillsA = evtable.EvTable(border="incols")
    table_skillsB = evtable.EvTable(border="incols")

    # Split dict list in half
    tableA = dict(list(caller.ndb._menutree.skills.items())
                  [:len(caller.ndb._menutree.skills) // 2])
    tableB = dict(list(caller.ndb._menutree.skills.items())
                  [len(caller.ndb._menutree.skills) // 2:])

    bonus_text = ''
    for skill in tableA:
        table_skillsA.add_row(skill.capitalize(),
                              skills.competency_desc(caller.ndb._menutree.skills[skill]))
    for skill in tableB:
        table_skillsB.add_row(skill.capitalize(),
                              skills.competency_desc(caller.ndb._menutree.skills[skill]))

    form.map(cells={
        1: name_string,
        2: "a short description",
        3: caller.ndb._menutree.age,
        4: caller.ndb._menutree.gender,
        5: caller.ndb._menutree.height,
        6: caller.ndb._menutree.weight}, tables={"A": table_skillsA, "B": table_skillsB})

    return (form, help_text), options


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

def _toggle_display(text, value, bool=True):
    bool_val = "|xNo|n"
    if bool:
        if value == True:
            bool_val = "|gYes|n"
    return f"{text} {bool_val}"

def _help(caller):
    """
    """
    pass


def _calculate_height(caller):
    """
    Randomize a character's height based on species min and max height values.
    60% chance to be average height
    20% chance to be either short or tall
    """

    height = random.uniform(caller.db.species.min_height,
                            caller.db.species.max_height)

    # is this a takula?
    if caller.db.species.name == 'Takula':
        # there is a 25% chance they are a Skink (short)
        if random.randint(0, 100) <= 25:
            caller.msg("|m{}|n |wis a Skink (a smaller, more dexterous, intelligent Takula). 25% of Takula are Skinks.|n".format(
                caller.ndb._menutree.name))
            # override species height defaults
            height = random.uniform(0.91, 1.40)

    stature_deviation = ['short'] * 20 + ['tall'] * 20 + ['average'] * 60
    stature = random.choice(stature_deviation)

    if stature == "short":
        height_var = random.uniform(-0.05, -0.15)
    elif stature == "tall":
        height_var = random.uniform(0.05, 0.15)
    else:
        height_var = 0.00

    height = height + height_var

    caller.ndb._menutree.height = format(height, ".2f")
    caller.ndb._menutree.height_desc = caller.db.species.height_description(
        height)

    _character_pane(caller)

