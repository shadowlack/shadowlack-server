"""
Characters

Characters are Objects setup to be puppeted by Accounts.
They are what you "see" in game.

"""
import re
import random

from django.urls import reverse

from evennia import DefaultCharacter
from evennia.utils import logger, ansi
from evennia.utils.utils import lazy_property, make_iter, variable_from_module

from evennia.contrib.rpsystem import RecogHandler, SdescHandler

from typeclasses.races import Pendragon

GENDER_PRONOUN_MAP = {
    "female": {"s": "she", "o": "her", "p": "her", "a": "hers"},
    "male": {"s": "he", "o": "him", "p": "his", "a": "his"},
    "neutral": {"s": "it", "o": "it", "p": "its", "a": "its"},
    "ambiguous": {"s": "they", "o": "them", "p": "their", "a": "theirs"},
}
RE_GENDER_PRONOUN = re.compile(r"(?<!\|)\|(?!\|)[sSoOpPaA]")


class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:
    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.
    """

    def web_get_detail_url(self):
        try:
            return reverse('sheet', kwargs={'object_id': self.db_key})
        except:
            return "#"

    def get_absolute_url(self):
        return reverse('sheet', kwargs={'object_id': self.db_key})

    def at_object_creation(self):
        """
        Called once when the character is first created.
        """

        super().at_object_creation()

        # appearance
        self.db.desc = "You see no one special."
        self.db.sdesc = "An unknown stranger"
        self.db.gender = "Ambiguous"
        self.db.age = 0
        self.db.height = 0
        self.db.weight = "Average"
        self.db.race = Pendragon()
        self.db.is_nullfire = False

        # information
        self.db.surname = None
        self.db.marital_status = "Single"
        self.db.allegiance = None
        self.db.is_awake = True

        self.db.khasi = 0
        self.db.bhijan = 0
        self.db.position = 'STANDING'

        # abilities
        self.db.abilities = {}
        self.db.can_get_pregnant = False
        self.db.is_sterile = False
        # nicknames
        self.db.nicks = {}

        self.db.pose_default = "is here."
        self.db.pose = self.db.pose or self.db.pose_default
        self.db.pose_death = 'lies dead.'
        self.db.pose_count = 0
        #  type/reset/force me = typeclasses.characters.Character

        self.db._sdesc = ""
        self.db._sdesc_regex = ""
        self.db._recog_ref2recog = {}
        self.db._recog_obj2regex = {}
        self.db._recog_obj2recog = {}

        @property
        def is_character(self):
            return True

        @property
        def race(self):
            return self.db.race.name if self.db.race else "Pendragon"

        def age_description(self):
            return self.db.race.age_description(self.db.age)

        def height_description(self):
            return self.db.race.height_description(self.db.height)

        @property
        def char_ob(self):
            return self

        def _get_pronoun(self, regex_match):
            """
            Get pronoun from the pronoun marker in the text. This is used as
            the callable for the re.sub function.
            Args:
                regex_match (MatchObject): the regular expression match.
            Notes:
                - `|s`, `|S`: Subjective form: he, she, it, He, She, It, They
                - `|o`, `|O`: Objective form: him, her, it, Him, Her, It, Them
                - `|p`, `|P`: Possessive form: his, her, its, His, Her, Its, Their
                - `|a`, `|A`: Absolute Possessive form: his, hers, its, His, Hers, Its, Theirs
            """
            typ = regex_match.group()[1]  # "s", "O" etc
            gender = self.attributes.get("gender", default="ambiguous")
            gender = gender if gender in (
                "female", "male", "neutral") else "ambiguous"
            pronoun = self.GENDER_PRONOUN_MAP[gender][typ.lower()]
            return pronoun.capitalize() if typ.isupper() else pronoun

    @lazy_property
    def sdesc(self):
        return SdescHandler(self)

    @lazy_property
    def recog(self):
        return RecogHandler(self)

    def get_display_name(self, looker, **kwargs):
        """
        Displays the name of the object in a viewer-aware manner.
        Args:
            looker (TypedObject): The object or account that is looking
                at/getting inforamtion for this object.
        Kwargs:
            pose (bool): Include the pose (if available) in the return.
        Returns:
            name (str): A string of the sdesc containing the name of the object,
            if this is defined.
                including the DBREF if this user is privileged to control
                said object.
        Notes:
            The RPCharacter version of this method colors its display to make
            characters stand out from other objects.
        """
        idstr = "(#%s)" % self.id if self.access(
            looker, access_type="control") else ""
        if looker == self:
            sdesc = self.key
        else:
            try:
                recog = looker.recog.get(self)
            except AttributeError:
                recog = None
            sdesc = recog or (hasattr(self, "sdesc")
                              and self.sdesc.get()) or self.key
        pose = " %s" % (self.db.pose or "is here.") if kwargs.get(
            "pose", False) else ""
        return "|c%s|n%s%s" % (sdesc, idstr, pose)
