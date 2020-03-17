"""
Shadowlack skills module.

This work is based on Fate Core System and Fate Accelerated Edition, products of Evil Hat Productions, LLC, developed, authored, and edited by Leonard Balsera, Brian Engard, Jeremy Keller, Ryan Macklin, Mike Olson, Clark Valentine, Amanda Valentine, Fred Hicks, and Rob Donoghue, and licensed for our use under the Creative Commons Attribution 3.0 Unported license.
"""
from math import ceil


class SkillException(Exception):
    def __init__(self, msg):
        self.msg = msg


_SKILL_DATA = {
    'athletics': {
        'name': 'Athletics',
        'desc': ("Physical fitness, agility, swimming, flying, and climbing."),
        'attack': False,
        'defend': True
    },
    'artistry': {
        'name': 'Artistry',
        'desc': ("Skill in crafts, precision tasks, aesthetics, and creativity."),
        'attack': False,
        'defend': False
    },
    'biotech': {
        'name': 'Biotech',
        'desc': ("Medicine, drugs, pathogens, first aid, prosthetics, and cyberware."),
        'attack': False,
        'defend': False
    },
    'contacts': {
        'name': 'Contacts',
        'desc': ("Proficiency in networking and making connections."),
        'attack': False,
        'defend': True
    },
    'corpwise': {
        'name': 'Corpwise',
        'desc': ("Corporate, high society, and business etiquette."),
        'attack': False,
        'defend': False
    },
    'deceive': {
        'name': 'Deceive',
        'desc': ("Lying, misdirecting, impersonating, seducing, and disguises."),
        'attack': False,
        'defend': False
    },
    'empathy': {
        'name': 'Empathy',
        'desc': ("Noticing shifts in mood, feeling object auras, and telepathy."),
        'attack': False,
        'defend': False
    },
    'fight': {
        'name': 'Fight',
        'desc': ("Melee weapons and unarmed fighting."),
        'attack': True,
        'defend': True
    },
    'fronima': {
        'name': 'Fronima',
        'desc': ("Skill in magic, machina crafting, enchanting, and connection to the spirit world."),
        'attack': True,
        'defend': True
    },
    'investigate': {
        'name': 'Investigate',
        'desc': ("Research, examining objects, and forensics."),
        'attack': False,
        'defend': False
    },
    'lore': {
        'name': 'Lore',
        'desc': ("Having knowledge and history of the world and objects."),
        'attack': False,
        'defend': False
    },
    'notice': {
        'name': 'Notice',
        'desc': ("Passively noticing details at a glance and general perception."),
        'attack': False,
        'defend': True
    },
    'physique': {
        'name': 'Physique',
        'desc': ("Strength of the body, toxin resistance, and endurance."),
        'attack': False,
        'defend': True
    },
    'pilot': {
        'name': 'Pilot',
        'desc': ("Driving motorized vehicles, drones, personal air craft, and space crafts."),
        'attack': True,
        'defend': True
    },
    'security': {
        'name': 'Security',
        'desc': ("Threat modeling, building layouts, protection, security and encryption protocols."),
        'attack': False,
        'defend': True
    },
    'shoot': {
        'name': 'Shoot',
        'desc': ("Projectile weapons and ranged accuracy."),
        'attack': True,
        'defend': False
    },
    'stealth': {
        'name': 'Stealth',
        'desc': ("Sneaking, avoiding detection, hacking, and being subtle."),
        'attack': False,
        'defend': True
    },
    'streetwise': {
        'name': 'Streetwise',
        'desc': ("Urban survival, black market, and street knowledge."),
        'attack': False,
        'defend': False
    },
    'technology': {
        'name': 'Technology',
        'desc': ("Engineering, electronics, software, and hardware."),
        'attack': False,
        'defend': False
    },
    'will': {
        'name': 'Will',
        'desc': ("Strength of the mind and Fronima resistance."),
        'attack': False,
        'defend': True
    }
}

ALL_SKILLS = ('athletics', 'artistry', 'biotech', 'contacts', 'corpwise', 'deceive', 'empathy', 'fight', 'fronima',
              'investigate', 'lore', 'notice', 'physique', 'pilot', 'security', 'shoot', 'stealth', 'streetwise', 'technology', 'will')


def skill_expertise_desc(character, level):
    if level >= 8:
        return "legendary"
    elif level == 7:
        return "epic"
    elif level == 6:
        return "fantastic"
    elif level == 5:
        return "superb"
    elif level == 4:
        return "great"
    elif level == 3:
        return "good"
    elif level == 2:
        return "fair"
    elif level == 1:
        return "average"
    elif level == 0:
        return "mediocre"
    elif level == -1:
        return "poor"
    else:
        return "terrible"


def load_skill(skill):
    """Retrieves an instance of a `Skill` class.
    Args:
        skill (str): case insensitive skill name
    Returns:
        (Skill): instance of the named Skill
    """
    skill = skill.lower()
    if skill in ALL_SKILLS:
        return Skill(**_SKILL_DATA[skill])
    else:
        raise SkillException('Invalid skill name.')


class Skill(object):
    """Represents a Skill's display attributes for use in character creation.
    Args:
        name (str): display name for skill
        desc (str): description of skill
    """

    def __init__(self, name, desc, base):
        self.name = name
        self.desc = desc
