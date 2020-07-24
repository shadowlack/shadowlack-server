import unittest

from evennia.commands.default.tests import CommandTest

from commands.character import CmdGender, CmdHatch
from typeclasses.characters import Character


class TestCmdGender(CommandTest):

    character_typeclass = Character

    def test_gender_empty(self):
        self.call(CmdGender(), "",
                  "Usage: gender female|male|neutral|ambiguous")

    def test_gender_invalid(self):
        self.call(CmdGender(), "garbage here",
                  "Usage: gender female|male|neutral|ambiguous")

    def test_gender_female(self):
        self.call(CmdGender(), "female", "Your gender was set to Female.")

    def test_gender_male(self):
        self.call(CmdGender(), "male", "Your gender was set to Male.")

    def test_gender_neutral(self):
        self.call(CmdGender(), "neutral", "Your gender was set to Neutral.")

    def test_gender_ambiguous(self):
        self.call(CmdGender(), "ambiguous",
                  "Your gender was set to Ambiguous.")
