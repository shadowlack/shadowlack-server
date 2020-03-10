"""
Object

The Object is the "naked" base class for things in the game world.

Note that the default Character, Room and Exit does not inherit from
this Object, but from their respective default implementations in the
evennia library. If you want to use this class as a parent to change
the other types, you can do so by adding this as a multiple
inheritance.

"""
from evennia import DefaultObject


class Object(DefaultObject):

    def at_object_creation(self):
        super().at_object_creation()
        self.db.pose = self.db.pose or self.db.default_pose

    def get_mass(self):
        # Default objects have 1 unit mass.
        mass = self.attributes.get('mass', 1)
        return mass + sum(obj.get_mass() for obj in self.contents)
