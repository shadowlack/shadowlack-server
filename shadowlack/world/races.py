from evennia.utils import fill


class RaceException(Exception):
    """Base exception class for races."""

    def __init__(self, msg):
        self.msg = msg


ALL_RACES = ('Anubi', 'Aquabat', 'Feydragon', 'Khell',
             'Lukuo', 'Pendragon', 'Takula', 'Yki')


def load_race(race):
    """Returns an instance of the named race class.
    Args:
        race (str): case-insensitive name of race to load
    Returns:
        (Race): instance of the appropriate subclass of `Race`
    """
    race = race.capitalize()
    if race in ALL_RACES:
        return globals()[race]()
    else:
        raise RaceException("Invalid race specified.")


def become_race(char, race):
    """Causes a character to "transform" into the named race.
    """
    if isinstance(race, Race):
        race = race.name

    race = load_race(race)
    char.db.race = race.name

    # apply race bonuses

    # apply race languages


def _format_bonuses(bonuses):
    """Formats a dict of bonuses as a string."""
    traits = list(bonuses.keys())
    if len(bonuses) > 2:
        output = ' , '.join("|y{}|n".format(t) for t in traits)
    else:
        output = ' and '.join("|y{}|n".format(t) for t in traits)
    return output


def _format_colours(colours):
    """Formats a dict of colours as a string."""
    traits = list(colours)
    if len(colours) > 2:
        trail = traits.pop(0)
        output = ', '.join("|w{}|n".format(t) for t in traits)
        output += ', and |w{}|n'.format(trail)
    else:
        output = ' and '.join("|w{}|n".format(t) for t in traits)
    return output


class Races():
    """Base class for race attributes"""

    def __init__(self):
        self.name = None
        self.pronounced = ""
        self.plural_name = None
        self.scientific_name = None
        self._desc = ""

        # race-specific
        self.colours = {}
        self.languages = {}
        self.bonuses = {}
        self.has_mutations = False
        self.is_playable = True
        self.homeworld = "Ramath-lehi"
        self.can_interbreed = True

        self.help_text = None
        self.h_perc = 0.00

    @property
    def desc(self):
        """Return a formatted description of the race."""
        desc = "|g{}|n\n".format(self.name)
        if self.pronounced:
            desc += "|=gPronounced [{}].|n\n".format(self.pronounced)
        desc += ("{}").format(self._desc)
        desc += '\n'
        if len(self.bonuses) > 0:
            desc += '\n\n'
            desc += ("{} start with {} to {}".format(
                self.plural_name,
                'bonuses' if len(self.bonuses) > 1 else 'a bonus',
                _format_bonuses(self.bonuses))
            )
        desc += '. \n'
        desc += '\n\n'
        if len(self.colours) >= 1:
            desc += ("{} may be found in the following {}: {}".format(
                self.plural_name,
                'colours' if len(self.colours) > 1 else 'colour',
                _format_colours(self.colours))
            )
            desc += '. '
        else:
            desc += ("{} may be found in any colour. ").format(self.plural_name)
        desc += 'They are often between |w{} and {} metres|n in height.'.format(
            str(self.min_height), str(self.max_height))
        desc += '\n\n'

        return desc

    @desc.setter
    def desc(self, value):
        self._desc = value

    def update(self):
        pass

    def at_look(self):
        return False

    def age_description(self, a):
        low, high = self.min_age, self.max_age
        a_perc = (a * 100) / high

        if a < low:
            return "hatchling"
        if a_perc >= 85:
            return "ancient"
        if a_perc >= 50:
            # kiom = elder male
            return "elderly"
        if a_perc >= 41:
            return "middle-aged"
        if a_perc >= 30:
            # Arden = adult male
            # thill = adult female
            return "adult"
        if a_perc >= 21:
            # Nioti = young male
            # Niotie = young female
            return "young adult"
        return "young"

    def height_description(self, h):

        h = float(h)
        low = float(self.min_height)
        high = float(self.max_height)

        avg_height = (low + high) / 2
        h_perc = ((h / high) * 100)

        if h < low:
            return "stunted"
        if h > high:
            return "unnaturally tall"
        if h_perc >= 100.00:
            return "impressive"
        if h_perc >= 95.00:
            return "tall"
        if h_perc >= 90.00:
            return "above-average"
        if h_perc >= 80.00:
            return "average"
        if h_perc >= 70.00:
            return "below-average"
        if h_perc >= 50.00:
            return "short"
        if h_perc >= 5.00:
            return "diminutive"
        else:
            return "unknown"


class Anubi(Races):
    def __init__(self):
        super().__init__()
        self.name = "Anubi"
        self.pronounced = "uh-noo bahy"
        self.plural_name = "Anubi"
        self.scientific_name = "draco sapiens anubidis"
        self.min_height = 1.70
        self.max_height = 2.23
        self.min_weight = 38.56
        self.max_weight = 81.65
        self.languages = {"Odyre"}
        self.bonuses = {'Biotech': 1, 'Lore': 1}
        self.desc = "|gAnubi|n are lithe and muscular creatures who thrive in extreme desert climates. They have sharp pointed ears and long, thin tails. Strong followers of tradition, their religion and xenophobia has caused them to isolate themselves.\n\nMost Anubi would do almost anything in order to keep their ancient and royal bloodlines pure and untainted. Some have been so strong in their beliefs that the bloodline should remain pure that they have gone about trying to keep it this way through illegal cloning and genetic alterations. \n\nOnce nearly driven to extinction from a genetically engineered plague, the Anubi are still few in number. Anubi are extremely susceptible to disease due to inbreeding."
        self.colours = {'tangerine', 'rust', 'beige',
                        'silver', 'tan', 'white', 'black'}
        # bonus lore, biotech


class Aquabat(Races):
    def __init__(self):
        super().__init__()
        self.name = "Aquabat"
        self.plural_name = "Aquabats"
        self.pronounced = "ak-wuh bat"
        self.scientific_name = "resaquatilis sapiens"
        self.min_height = 1.65
        self.max_height = 2.00
        self.min_weight = 38.56
        self.max_weight = 72.57
        # bonus athletics, notice
        # can change gender
        # can breathe underwater
        self.can_interbreed = False
        self.bonuses = {'Athletics': 1, 'Notice': 1}
        self.desc = "|gAquabats|n are amphibious, and spend a majority of their life in oceans, seas, inlets, and freshwater lakes. They have evolved features such as echolocation and sex-shifting to suit their aquatic environments. They have delicate features with sharp snouts and sensitive facial whiskers for seeking prey in murky waters. Their entire body is streamlined for quick swimming. Useful webbed hands and feet, as well as a rudder-like tail. Some have fins that extend off the tail, which, combined with shoulder or underarm wingspans, aid in underwater movement.\n\nAquabats have slim air bladders beneath their skin which help them float, or sink, depending on to what degree they are inflated. They have the ability to breathe through their skin, an innovation that enables them to venture safely on either land or water.\n\nFemales carry the eggs in a pouch instead of leaving them in a nest, where they could be eaten, or otherwise wash away."
        self.colours = {'green', 'blue', 'violet', 'purple', 'black'}


class Feydragon(Races):
    def __init__(self):
        super().__init__()
        self.name = "Feydragon"
        self.pronounced = "fey drag-uh n"
        self.plural_name = "Feydragons"
        self.scientific_name = "draco sapiens pauxillulus"
        self.min_height = 0.69
        self.max_height = 1.10
        self.min_weight = 6.80
        self.max_weight = 27.00
        # bonus fronima, empathy
        self.has_mutations = True
        self.bonuses = {'Fronima': 1, 'Empathy': 1}
        self.desc = "|gFeydragons|n are an ancient subspecies with deep ties to the magic they wield, Feydragons are as widely varied as there are many kinds of magic. Most notably, the Fey are smaller; on average and when fully-grown, quadrupeds are no bigger than the red fox of late Earth, and bipeds are no taller than 1.10 metres. Fey often refer to Pendragons as tall, even if the Pendragon in question is considered short by their peers.\n\nFey always have wings and tail-flames. Fey wings are one of the most varied parts of their appearance; wings that would be biologically impossible, yet are capable of working, are not uncommon.\n\nNearly all Fey sport special Fronima-infused tattoos, often related to their bloodlines.\n\nA Feydragon must have one of the following subtypes:\n\n1.) |gKynnyn|n and |gMongrel Kynnyn|n are the most common type of Fey and are the most integrated with Ramathian society. 80% of Feydragons are of this type. Kynnyn are generalists and hold no affinity to any particular element of magic. Due to their lack of specialization, they have the ability to become more powerful than any of the other Fey subtypes. Most Kynnyn are multi-talented and often take things that others view as hobbies or or pastimes competitively.\nMongrel Kynnyn are made up of hybrids and Fey from other groups who abandoned their heritage. The practice of sending such individuals to live in Kynnyn clans is an old one, going back thousands of years.\n\n2.) |gAlanamsul|n (elemental) are the second most common subtype of Feydragon and account for 11% of the Fey population. They are followers of the religion Tanalism and specifically worship the six elemental Numegola and refer to themselves as that deity's children. Every Alanamsul's appearance is influenced by its chosen Numegola. For example, a Child of Reda will primarily take on the appearance of fire.\n\n3.) |gAzetsum|n are known for their preternatural beauty and account for 6% of the Fey population. They are so divine in appearance that they are often called angels and are universally regarded as attractive by the Ramathian population. Some wonder if they were deliberately bred for physical appearance or passively charm all those around themselves.\nAzetsum are taller than all other types of Fey, and are much more muscular looking. They are always light in colour, and sometimes have darker markings (e.g. white with black stripes or spots). The wings of the Azetsum resemble those of giant feathered birds.\nAll this, along with a culture that centres largely on worship of Tanastlasei and Fromina, has given the Azetsum an image of kindly, noble, and beautiful \"divine champions\" who struggle for the continued existence of Ramath-lehi and its people.\n\n4.) |gMyshemd|n are the most misunderstood type of Fey and make up the remaining 4% of the population. As if they exist only to contrast the Azetsum, the Myshemd are nightmarish in appearance. These demon-like Fey are often stereotyped as evil and nihilistic worshippers of Kytlekh. Myshemd come in dark colours, and sometimes have light markings (e.g. dark red with acid yellow spots). Their wings come in two different varieties: males have bat-like webbed wings, while females have bat-wings that are covered in feathers.\n\n"


class Khell(Races):
    def __init__(self):
        super().__init__()
        self.name = "Khell"
        self.pronounced = "kel"
        self.plural_name = "Khellin"
        self.scientific_name = "draco sapiens terragelatum"
        self.min_height = 1.80
        self.max_height = 2.40
        self.min_weight = 150.00
        self.max_weight = 250.00
        self.languages = {"Khellakh"}
        self.bonuses = {'Technology': 1, 'Fight': 1}
        # bonus technology, fight
        # penalty in warm places (heavy insulating fur)


class Lukuo(Races):
    def __init__(self):
        super().__init__()
        self.name = "Lukuo"
        self.pronounced = "loo hwoh"
        self.plural_name = "Lukuo"
        self.scientific_name = "draco sapiens mutabilis"
        self.min_height = 1.65
        self.max_height = 2.18
        self.min_weight = 45.35
        self.max_weight = 158.76
        # bonus fronima, will
        self.has_mutations = True


class Pendragon(Races):
    def __init__(self):
        super().__init__()
        self.name = "Pendragon"
        self.pronounced = "pen drag-uh n"
        self.plural_name = "Pendragons"
        self.scientific_name = "draco sapiens"
        self.min_height = 1.65
        self.max_height = 2.18
        self.min_weight = 45.35
        self.max_weight = 158.76
        self.bonuses = {'Pilot': 1, 'Physique': 1}
        # bonus physique, pilot
        # generic most "human-like" race


class Rapine(Races):
    def __init__(self):
        super().__init__()
        self.name = "Rapine"
        self.plural_name = "Rapine"
        self.scientific_name = "bloody bastards"
        self.min_height = 2.10
        self.max_height = 2.80
        self.is_playable = False
        self.homeworld = "Vaiuto"
        # soul suckers
        self.can_interbreed = False


class Takula(Races):
    def __init__(self):
        super().__init__()
        self.name = "Takula"
        self.plural_name = "Takula"
        self.scientific_name = "draco sapiens lacerta"
        self.min_height = 1.83
        self.max_height = 2.53
        self.min_weight = 68.00
        self.max_weight = 113.00
        self.languages = {"Takola"}
        self.bonuses = {'Physique': 1, 'Fight': 1}
        # bonus physique, fight
        self.can_interbreed = False


class Yki(Races):
    def __init__(self):
        super().__init__()
        self.name = "Yki"
        self.plural_name = "Yki"
        self.scientific_name = "draco sapiens albusglacies"
        self.min_height = 1.30
        self.max_height = 2.18
        self.min_weight = 0
        self.max_weight = 0
        self.languages = {"Ykili"}
        self.bonuses = {'Artistry': 1, 'Deceive': 1}
        # bonus artistry, deceive


"""
Very rare
Anubi x Yki (extremely rare)
Anubi x Khell (extremely rare)
Anubi x Feydragon (rare)
Anubi x Lukuo (rare)
Anubi x Pendragon (rare)


Rare

Feydragon x Khell (extremely rare)
Feydragon x Lukuo (rare)
Feydragon x Pendragon (rare)
Feydragon x Yki (extremely rare)

Khell x Lukuo
Khell x Pendragon

Lukuo x Pendragon
Lukuo x Yki

Khell x Yki (rare)
Yki x Pendragon
"""
