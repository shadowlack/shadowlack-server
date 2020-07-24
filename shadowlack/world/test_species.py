"""
Species test module.
"""

from django.test import TestCase
from evennia.utils.test_resources import EvenniaTest
from typeclasses.characters import Character
from world import species

class LoadSpeciesTestCase(TestCase):
    """
    This is important because we want to ensure that 
    species bonuses have been properly applied.
    """

    def test_anubi(self):
        anubi = species.load_species('Anubi')
        self.assertEqual(anubi.name, 'Anubi')
        self.assertEqual(anubi.bonuses, {'biotech': 3, 'lore': 3})

    def test_aquabat(self):
        aquabat = species.load_species('Aquabat')
        self.assertEqual(aquabat.name, 'Aquabat')
        self.assertEqual(aquabat.bonuses, {'athletics': 3, 'notice': 3})

    def test_feydragon(self):
        feydragon = species.load_species('Feydragon')
        self.assertEqual(feydragon.name, 'Feydragon')
        self.assertEqual(feydragon.bonuses, {'fronima': 3, 'empathy': 3})

    def test_khell(self):
        khell = species.load_species('Khell')
        self.assertEqual(khell.name, 'Khell')
        self.assertEqual(khell.bonuses, {'technology': 3, 'fight': 3})

    def test_lukuo(self):
        lukuo = species.load_species('Lukuo')
        self.assertEqual(lukuo.name, 'Lukuo')
        self.assertEqual(lukuo.bonuses, {'fronima': 3, 'will': 3})

    def test_pendragon(self):
        pendragon = species.load_species('Pendragon')
        self.assertEqual(pendragon.name, 'Pendragon')
        self.assertEqual(pendragon.bonuses, {'pilot': 3, 'physique': 3})
    
    def test_takula(self):
        takula = species.load_species('Takula')
        self.assertEqual(takula.name, 'Takula')
        self.assertEqual(takula.bonuses, {'physique': 3, 'fight': 3})

    def test_yki(self):
        yki = species.load_species('Yki')
        self.assertEqual(yki.name, 'Yki')
        self.assertEqual(yki.bonuses, {'artistry': 3, 'deceive': 3})

