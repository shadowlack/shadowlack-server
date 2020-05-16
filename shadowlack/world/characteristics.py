class Characteristic:
    def __init__(self, name):
        self.name = name

class CharacteristicException(Exception):
    """Base exception class for characteristics."""
    def __init__(self, msg):
        self.msg = msg

class CharacteristicHandler:
    def __init__(self, character):
        self.character = character

    def init_characteristics(self):
        if self.character.db.characteristics is None:
            self.character.db.characteristics = {}

'''

Feydragon
- Kynnyn (Generalists)
- Alanamsul (Elemental)
- Azetsum (Angelic) + feathered wings
- Myshemd (Demonic) + bat wings

Mutations
- Multiple arms
- Multiple legs
- Multiple wings
- Extra fingers
- Extra toes
- Extra eyes
- Extra ears
- Horns
- Tusks
- Bone spikes
- Quills
- Multiple tails
- Tail blade
- Tail flame
- Long limbed

Reproduction
- Get others pregnant
- Get pregnant
- Sterile (nullifies other options)

Magic
- Nullfire (cannot do magic)

Magia Morbii (Magical Diseases)
- Dermallaghica
- Falters Skele
- Kycgeja-Kycyja-Gjytkeoduja (KKG)
- Magihaematophagia
- Magimetachrosis
- Therianthropy
- Vampirism

'''
