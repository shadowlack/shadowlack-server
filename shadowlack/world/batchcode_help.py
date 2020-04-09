# shadowlack/world/batchcode_help.py
# run as super user:
# batchcode batchcode_help

# HEADER

from evennia import create_help_entry
from world import skills

# CODE

# Add skills to help system
for skill in skills.ALL_SKILLS:
    skill = skills.load_skill(skill)

    skill_types = ''

    # Add indicator for if this skill can be used to attack and/or defend
    if skill.attack or skill.defend:
        skill_types += ' This skill can be used to '
        if skill.attack:
            skill_types += "Attack"
        if skill.attack and skill.defend:
            skill_types += ' and '
        if skill.defend:
            skill_types += "Defend"
        skill_types += '.'

    skill_entry = create_help_entry(skill.name.lower(), skill.desc + skill_types, category="Skills", locks="view:all()")

    if skill_entry:
        caller.msg("{} added to Help.".format(skill.name))

# CODE

# Lexicon