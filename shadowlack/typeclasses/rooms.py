"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom
from evennia.contrib.rpsystem import ContribRPRoom


class Room(ContribRPRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.x = 0
        self.db.y = 0
        self.db.z = 0

        self.db.zone = None
        self.db.environment = None
        self.db.temperature = 30

        # Can the general public see or overhear?
        # Insecure communication to key actions
        self.db.is_public = True

    @property
    def is_room(self):
        return True

    # Are there characters here?
    @property
    def player_characters(self):
        return [ob for ob in self.contents if hasattr(ob, "is_character") and ob.is_character and ob.player]

    # gGet visible characters in room
    def get_visible_characters(self, pobject):
        return [char for char in self.player_characters if char.access(pobject, "view")]

    # weather
    # residents/homeowner


class IndoorRoom(Room):

    @property
    def is_indoors(self):
        return True


class VacuumRoom(Room):

    @property
    def is_vacuum(self):
        return True


class UnderwaterRoom(Room):

    @property
    def is_underwater(self):
        return True
