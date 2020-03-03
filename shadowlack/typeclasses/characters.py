"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from django.urls import reverse

from evennia import DefaultCharacter
from evennia.contrib.rpsystem import ContribRPCharacter
import random


class Character(ContribRPCharacter):

    def web_get_detail_url(self):
        try:
            return reverse('sheet', kwargs={'object_id': self.db_key})
        except:
            return "#"

    def at_object_creation(self):
        """
        Called once when the object is created.
        """
        super(Character, self).at_object_creation()

        self.db.desc = "You see nothing special."

        sdescList = ["A shady looking character",
                     "A regular Pendragon", "A potentially magical being", "Someone you should talk to", "A shrouded mystery", "A friendly face"]

        self.db._sdesc = random.choice(sdescList)

        self.db.race = None
        self.db.surname = None
        self.db.gender = "ambiguous"

        self.db.wallet = {"Khasi": 0, "Bhijan": 0}
        self.db.position = 'STANDING'
        self.db.pose = self.db.pose or self.db.pose_default
        self.db.pose_death = 'lies dead.'


class NPC(Character):
    """
    Base character typeclass for NPCs and enemies.
    """
    #super(NPC, self).at_object_creation()
    pass
