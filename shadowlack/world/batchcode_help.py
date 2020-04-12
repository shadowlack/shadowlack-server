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

# Phrases
phrases = [
    {
        'name': ("A Grader's Way"),
        'desc': ("To die suddenly and/or by possible conspiracy. The Graders are a powerful political family that gets blamed for a lot of negative things.")
    },
    {
        'name': 'A square wheel',
        'desc': 'Something or someone that is useless.'
    },
    {
        'name': 'Beaten Fronnaless',
        'desc': 'To be beaten to a pulp!'
    },
    {
        'name': 'Handled that like a gaukh',
        'desc': ("Used to colourfully describe another's inability to keep a level head; also pertains to one's fiery attitude in the presence of another or group. Extremely rebellious 'dragons - often teens - are talked to like this.")
    },
    {
        'name': 'Impaled Sunset',
        'desc': 'Looming death.'
    },
    {
        'name': ("Like a hatchling's breath"),
        'desc': ("The opposite of a blessing in disguise. It's wonderful at first but then after time you realize it's unpleasant.")
    },
    {
        'name': 'Liraxed away',
        'desc': ("To lirax someone. To die without any forewarning, and quite mysteriously/to kill one quietly, quickly, and without a trace.")
    },
    {
        'name': 'Luceshtaf Fruiter',
        'desc': ("Someone who tries to please everyone, never going against anything. It comes from the fact that the fruit of a luceshtaf will taste pleasant to everyone, as it tastes like whatever the persons favorite food or drink is. Luceshtaf fruiter is generally used to describe politicians who try to please every political party.")
    },
    {
        'name': ("Of a Rapine's Feather"),
        'desc': ("A more or less polite, and perhaps aristocratic way, of calling someone an asshole.")
    },
    {
        'name': 'Paint your scars',
        'desc': ("To recover from and move on from a traumatic incident or a difficult time in one's life.")
    },
    {
        'name': 'Road of Visions',
        'desc': ("Nothing is quite what it appears to be.")
    }
]

for phrase in phrases:
    phrase_entry = create_help_entry(phrase['name'].lower(), phrase['desc'], category="Phrasebook", locks="view:all()")

if phrase_entry:
    caller.msg("{} added to Help.".format(phrase['name']))

# CODE

words = [
    {
        'name': ("Arden"),
        'desc': ("A fully grown adult male.")
    },
    {
        'name': ("Thill"),
        'desc': ("A fully grown adult female.")
    },
    {
        'name': ("Fronima"),
        'desc': ("1.) An energy source used for magic and machina. 2.) Where the souls of deceased Pendragons go (unless they are killed by a Rapine). 3.) The world in which nightmares and dreams exist.")
    },
    {
        'name': ("Fronna"),
        'desc': ("Slang. A slang term for the word Fromina. Often used as an interjection. 'For Fronna's sake!' Believed to have come from lazy kids who thought that three syllables were too many.")
    },
    {
        'name': ("Machina"),
        'desc': ("Machines that are run using magicka (Fronima) as their power source.")
    },
    {
        'name': ("Magicka"),
        'desc': ("The common name for the power source of machina. Much like machines on our Earth are run by electricity, machina is powered by magicka.")
    },
    {
        'name': ("Hatchling"),
        'desc': ("An newly hatched or very young individual, or someone who is displaying childish behaviour.")
    },
    {
        'name': ("Nioti"),
        'desc': ("A young male Ramathian. Could also be used as an insult.")
    },
    {
        'name': ("Niotie"),
        'desc': ("A young female Ramathian. Could also be used as an insult.")
    },
    {
        'name': ("Numegola"),
        'desc': ("A numegola is a god or goddess that is related to (or can manipulate) a specific element. eg. The god Renn-nukhs is the Numegola of Air.")
    }
]

for word in words:
    word_entry = create_help_entry(word['name'].lower(), word['desc'], category="Lexicon", locks="view:all()")

    if word_entry:
        caller.msg("{} added to Help.".format(word['name']))

# CODE

honorifics = [
    {
        'name': ("Arch Magos"),
        'desc': ("Masculine. Used as a title and form of address for both past and present male sovereigns of Ramath-lehi.")
    },
    {
        'name': ("Arch Magosai"),
        'desc': ("Feminine. Used as a title and form of address for both past and present female sovereigns of Ramath-lehi.")
    },
    {
        'name': ("Ba"),
        'desc': ("Suffix. Usually used for an instructor/teacher or superior; usually applied to a surname.")
    },
    {
        'name': ("Ni"),
        'desc': ("Suffix. Usually used with significant others, loved ones, and children; indicates a very close bond and is always used with the first name or nickname. Usage: Trei'ni, addressing a character named Treimaline with the nickname Trei. ")
    },
    {
        'name': ("Kiom"),
        'desc': ("A respectful term for an elder male Ramathian who is above the age of 50. The term is generally not used for females and may be taken offensively. An insult to anyone who is obviously under the age of 50.")
    },
    {
        'name': ("De"),
        'desc': ("Archaic) Prefix. Traditionally used with one's surname to indicate being a member of a noble bloodline. Integrated into some modern surnames. Usage: Oxlar de'Goerduan; addressing a character named Oxlar and acknowledging them as a member of the Goerduan family.")
    },
    {
        'name': ("Sla"),
        'desc': ("Suffix. An affectionate pet name for loved ones (children or significant others). Usage: Tsuj'sla – addressing a loved one with the first name Tsuj.")
    }
]
for honorific in honorifics:
    honorific_entry = create_help_entry(honorific['name'].lower(), honorific['desc'], category="Honorifics", locks="view:all()")

    if honorific_entry:
        caller.msg("{} added to Help.".format(honorific['name']))

# CODE

humilifics = [
    {
        'name': ("Kyttle-lover"),
        'desc': ("Derogatory. Someone who worships Kytlekh. A mean, nasty, bad person. Derogatory and highly insulting slang.")
    },
    {
        'name': ("Keita"),
        'desc': ("(Anubian) Derogatory. A traitor. Specifically an Anubi who has committed treason by producing halfbreed offspring.")
    },
    {
        'name': ("Vultarjuem"),
        'desc': ("Derogatory. A know-it-all; a smart-ass.")
    },
    {
        'name': ("Pet Rapine"),
        'desc': ("Derogatory. Someone who seems nice, but is actually far from well-meaning.")
    },
    {
        'name': ("Nullfire"),
        'desc': ("Derogatory. Someone who lacks magical heritage or power. Also nilflame, nilfire, and nullflame.")
    },
    {
        'name': ("Fur-scale"),
        'desc': ("(Takola) Sometimes derogatory. A word used by some Takula to refer to non-Takula Ramathians.")
    },
]

for humilific in humilifics:
    humilific_entry = create_help_entry(humilific['name'].lower(), humilific['desc'], category="Humilifics", locks="view:all()")

    if humilific_entry:
        caller.msg("{} added to Help.".format(humilific['name']))

# CODE

vulgarities = [
    {
        'name': ("Karshäch"),
        'desc': ("(Khellin) Vulgar. The Khellakh equivalent of the English profanity bullshit.")
    },
    {
        'name': ("Vaak"),
        'desc': ("(Shublavaak) Vulgar, Interjection. The Ramathian equivalent of the English profanity shit. 1. noun. feces. 2. verb. act of defecating. 3. Slang. noun. Lies, worthless information. 4. Slang. adjective. Worthless, inferior. 5. Slang. narcotic drugs. 6. Slang. possessions, equipment, mementos, etc.; stuff.")
    },
    {
        'name': ("Kyttle"),
        'desc': ("(Kytlekh) Vulgar. Derogatory slang. Why do you have to be so Kyttle (nasty)?")
    }
]

for vulgarity in vulgarities:
    vulgarity_entry = create_help_entry(vulgarity['name'].lower(), vulgarity['desc'], category="Vulgarities", locks="view:all()")

    if vulgarity_entry:
        caller.msg("{} added to Help.".format(vulgarity['name']))

# Climate

seasons = [
    {
        'name': ("Dyo"),
        'desc': ("Spring. The second of Ramath-lehi's four seasonal quarters.")
    },
]

# Languages
languages = [

]

# Families
families = [
    {
        'name': ("Dragyn"),
        'desc': ("The well known last name of Pendragons that seem to get in over their heads when it comes to trouble.")
    },
    {
        'name': ("Grader"),
        'desc': ("One belonging to the royal Grader bloodline. Notable figures include the late Arch Magos Zamfir Grader, the late Arch Magosai Karryasa Grader, Lakmir Grader and Koani Grader.")
    },
]