"""
Skills test module.
"""

from django.test import TestCase
from evennia.utils.test_resources import EvenniaTest
from typeclasses.characters import Character
from world import skills


class LoadSkillTestCase(TestCase):

    def test_athletics(self):
        skill = skills.load_skill('athletics')
        self.assertEqual(skill.name, 'Athletics')
        self.assertIsNotNone(skill.desc)
        self.assertFalse(skill.attack)
        self.assertTrue(skill.defend)

    def test_artistry(self):
        skill = skills.load_skill('artistry')
        self.assertEqual(skill.name, 'Artistry')
        self.assertIsNotNone(skill.desc)
        self.assertFalse(skill.attack)
        self.assertFalse(skill.defend)

    def test_biotech(self):
        skill = skills.load_skill('biotech')
        self.assertEqual(skill.name, 'Biotech')
        self.assertIsNotNone(skill.desc)
        self.assertFalse(skill.attack)
        self.assertFalse(skill.defend)

    def test_contacts(self):
        skill = skills.load_skill('contacts')
        self.assertEqual(skill.name, 'Contacts')
        self.assertIsNotNone(skill.desc)
        self.assertFalse(skill.attack)
        self.assertTrue(skill.defend)

    def test_corpwise(self):
        skill = skills.load_skill('corpwise')
        self.assertEqual(skill.name, 'Corpwise')
        self.assertIsNotNone(skill.desc)
        self.assertFalse(skill.attack)
        self.assertFalse(skill.defend)

    def test_deceive(self):
        skill = skills.load_skill('deceive')
        self.assertEqual(skill.name, 'Deceive')
        self.assertIsNotNone(skill.desc)
        self.assertFalse(skill.attack)
        self.assertTrue(skill.defend)

    def test_empathy(self):
        skill = skills.load_skill('empathy')
        self.assertEqual(skill.name, 'Empathy')
        self.assertIsNotNone(skill.desc)
        self.assertFalse(skill.attack)
        self.assertTrue(skill.defend)

    def test_fight(self):
        skill = skills.load_skill('fight')
        self.assertEqual(skill.name, 'Fight')
        self.assertIsNotNone(skill.desc)
        self.assertTrue(skill.attack)
        self.assertTrue(skill.defend)

    def test_fronima(self):
        skill = skills.load_skill('fronima')
        self.assertEqual(skill.name, 'Fronima')
        self.assertIsNotNone(skill.desc)
        self.assertTrue(skill.attack)
        self.assertTrue(skill.defend)

    def test_investigate(self):
        skill = skills.load_skill('investigate')
        self.assertEqual(skill.name, 'Investigate')
        self.assertIsNotNone(skill.desc)
        self.assertFalse(skill.attack)
        self.assertFalse(skill.defend)

    def test_lore(self):
        skill = skills.load_skill('lore')
        self.assertEqual(skill.name, 'Lore')
        self.assertIsNotNone(skill.desc)
        self.assertFalse(skill.attack)
        self.assertFalse(skill.defend)

    def test_notice(self):
        skill = skills.load_skill('notice')
        self.assertEqual(skill.name, 'Notice')
        self.assertEqual(skill.attack, False)
        self.assertEqual(skill.defend, True)

    def test_physique(self):
        skill = skills.load_skill('physique')
        self.assertEqual(skill.name, 'Physique')
        self.assertIsNotNone(skill.desc)
        self.assertFalse(skill.attack)
        self.assertTrue(skill.defend)

    def test_pilot(self):
        skill = skills.load_skill('pilot')
        self.assertEqual(skill.name, 'Pilot')
        self.assertIsNotNone(skill.desc)
        self.assertTrue(skill.attack)
        self.assertTrue(skill.defend)

    def test_security(self):
        skill = skills.load_skill('security')
        self.assertEqual(skill.name, 'Security')
        self.assertIsNotNone(skill.desc)
        self.assertFalse(skill.attack)
        self.assertTrue(skill.defend)

    def test_shoot(self):
        skill = skills.load_skill('shoot')
        self.assertEqual(skill.name, 'Shoot')
        self.assertIsNotNone(skill.desc)
        self.assertTrue(skill.attack)
        self.assertFalse(skill.defend)

    def test_stealth(self):
        skill = skills.load_skill('stealth')
        self.assertEqual(skill.name, 'Stealth')
        self.assertIsNotNone(skill.desc)
        self.assertFalse(skill.attack)
        self.assertTrue(skill.defend)

    def test_streetwise(self):
        skill = skills.load_skill('streetwise')
        self.assertEqual(skill.name, 'Streetwise')
        self.assertIsNotNone(skill.desc)
        self.assertFalse(skill.attack)
        self.assertFalse(skill.defend)

    def test_technology(self):
        skill = skills.load_skill('technology')
        self.assertEqual(skill.name, 'Technology')
        self.assertIsNotNone(skill.desc)
        self.assertFalse(skill.attack)
        self.assertFalse(skill.defend)

    def test_will(self):
        skill = skills.load_skill('will')
        self.assertEqual(skill.name, 'Will')
        self.assertIsNotNone(skill.desc)
        self.assertFalse(skill.attack)
        self.assertTrue(skill.defend)
