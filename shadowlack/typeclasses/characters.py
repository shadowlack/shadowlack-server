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

        self.db.msgcolour = True

        # appearance
        self.db.desc = "You see no one special."
        self.db.sdesc = "An unknown stranger"
        self.db.gender = "Ambiguous"
        self.db.age = 18

        # information
        self.db.surname = "None"
        self.db.marital_status = "Single"
        self.db.allegiance = "None"
        self.db.health_status = "Alive"
        self.db.sleep_status = "Awake"

        self.db.wallet = {"Khasi": 0, "Bhijan": 0}
        self.db.position = 'STANDING'
        self.db.pose_default = "is here."
        self.db.pose = self.db.pose or self.db.pose_default
        self.db.pose_death = 'lies dead.'
        self.db.pose_count = 0
        #  type/reset/force me = typeclasses.characters.Character

        @property
        def is_character(self):
            return True

        @property
        def race(self):
            return self.db.race or "Pendragon"

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
