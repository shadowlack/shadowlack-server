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
        self.bonuses = {'biotech': 3, 'lore': 3}
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
        self.bonuses = {'athletics': 3, 'notice': 3}
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
        self.bonuses = {'fronima': 3, 'empathy': 3}
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
        self.bonuses = {'technology': 3, 'fight': 3}
        # bonus technology, fight
        # penalty in warm places (heavy insulating fur)
        self.desc = "|gKhellin|n are native to the frigid Trilok continent. Khellin were thought to have been born from the frozen mountain earth, as they would often spring forth from their subterranean labyrinthine mega-cities to surprise foes. \n\nUnlike their lithe northern Yki cousins, Khellin have stocky and muscular builds with small ears and short tails. They are larger and weigh more than the average Pendragon due to their bone structure. Khellin have evolved to fit a very specific ecological niche, with many body characteristics adapted for extremely cold temperatures. They are insulated by several inches of blubber and have superbly dense underfur. Longer guard-hairs (up to 15 cm long for females and 40 cm for males) adorn their arms, legs, and ears, for extra warmth. It is not uncommon for Khellin to shave their fur when visiting or living in warmer climates, as they are prone to overheating in temperatures above 15 °C. When exposed to extremely cold temperatures, Khellin secrete special oils which makes their fur even less susceptible to frost. It is these oils that make their fur very soft and luxurious to the touch.\n\nKhellin are highly carnivorous and are unable to survive on a vegetarian diet. They possess large scooped claws which are amazing for digging through earth and ice, and have special molars that allow them to rip apart meat or carrion that has been frozen solid."


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
        self.desc = "|gLukuo|n come in a variery of heavy genetic mutations. These mutations usually show up as extra growths on a Pendragon's body which are generally in the form of horns, spikes, mis-matched wings, multiple wings, fingers, toes, or other appendages.\n\nThe Lukuo are a branch off of the Pendragon race, and of all the known branches, they are the most closely related to the Pendragon. Lukuo mutations are recessive in the genetic makeup, and therefore are not common, however as the Pendragon race continues to evolve, certain mutations become more common over time. Lukuo genes need to be triggered in some way to appear in progeny, either by another Lukuo recessive gene in the other parent, or in the absence of a gene, in which case the mutation will surface, because there is no dominant gene to suppress it.\n\nLukuo are identified by any number of extra or multiple body decorations. These include multiple limbs and tails, any number and type of horns on their skull, or bone spikes manifesting themselves anywhere on the body, but most commonly along the spine, shoulder blades, elbows, and ankles. Wings are a growing common sight among Pendragons, but multiple wings, often one atop the other, or one pair in front of another pair also denote a Lukuo. (Often one pair is smaller than the other.) In the case of a single pair of bat or dragon wings, multiple 'thumbs' or 'fingers' also constitute a Lukuo."


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
        self.bonuses = {'pilot': 3, 'physique': 3}
        # bonus physique, pilot
        # generic most "human-like" race
        self.desc = "|gPendragons|n are the most dominant species on Ramath-lehi. They are an anthropomorphic mix of feline, canine, and dragon. Because of their genetic makeup, the variety among these individuals is astounding.\n\nPendragon colours can range dramatically, as they have taken on all of the hues of the visible light spectrum. So it is not uncommon to see a green Pendragon, or even one with rainbow-coloured stripes. Their body structure is similar to that of a wolf, although entwined with a lot of feline attributes - some even look a lot like Earth's big cats, or even like true mythological dragons. They usually have hair growing from the top of their heads that sometimes slinks down their backs like soft spikes, or even bladed hair.\n\nIn terms of physiological differences between the sexes, there are not very many. Both male and female Pendragons are capable of telepathic thought-speak (sending messages into each other's minds). This is not the prefered method of communication, but it is still used, nonetheless. However, male Pendragons commonly carry flames at the end of their tails although finding this mutation in females is not extremely rare. These flames are often reflective of a Pendragon's mood or strength.\n\nMost Pendragons are marked with tattoos, usually on their left haunch, although sometimes on the right. These are symbols that their parents thought would reflect the young Pendragon's personality. Usually the parents consult a seer or someone else of that nature in order to gain insight as to what a Pendragon's symbol should be. Some players like to make up random designs for their character's tattoo, or even base them off of a specific creature or object."


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
        self.desc = "|gRapine|n"


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
        self.bonuses = {'physique': 3, 'fight': 3}
        # bonus physique, fight
        self.can_interbreed = False
        self.desc = "|gTakula|n are powerful, towering reptilians that are found in the remote jungles and dense forests of Ramath-lehi.\n\nTheir colours are specific, they include, blue, orange, red, green, purple, yellow and magenta. They always have one main colour and a second colour. The second colours is for their fins and scale patterns. They do not have to have a secondary colour though, and some times they have other colours as well aside from their main ones.\n\nTakula have no fur whatsoever. They are covered in scales that are often very bright and vivid in colours that range from tropical greens to vibrant oranges and reds. Their hands are large and made up of two thick fingers and an opposable thumb. All fingers have wicked two-inch claws on them that can be re-grow if broken and are very helpful for climbing trees and stone surfaces. Their heads often vary quite a bit from individual to individual. They range from having different sized horns to brightly coloured fins or even quills running down the backs of their heads. Takula all have thick tails with the same rules of tail flames as a normal Pendragon, some however have spikes and/or extruding bones showing.\n\nAbout one in four Takula are born with a defect that makes them very small, these defected ones are only about three feet high but are much more dexterous and faster than the average Takula. These smaller Takula are commonly called Skinks. Skinks are smarter than average, being able to build and work more complex ideas in their heads. Since they are smarter, they often fill out the role of priests or shamans in the tribe. Apart from females, they are the only ones capable of handling magic."


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
        self.bonuses = {'artistry': 3, 'deceive': 3}
        # bonus artistry, deceive
        self.desc = "|gYki|n thrive in the bitter north. Adept masters of the terrains they frequent, these northern Pendragons do not need the advanced technology used throughout the more southern climates to thrive and live comfortably.\n\nThe Yki (a name given by those learnt Pendragons who first discovered the natives of Dhruv) tend to be small and fox-like at first glance. Their pelts consist of a thick, downy undercoat that traps heat against the body and a long, wiry outer coat that is made up of hollow hairs that capture and retain heat. They have large ears, but their hair grows especially long around them, sheltering the sensitive organs from frostbite. The Yki are also able to fold back their ears, tucking them into the thick fur of the back of their head if needed; their ears are incredibly flexible, thanks to well-formed muscles at their bases. The leather of their noses is almost always black, the only individuals with pink or pale nose leather being albinos and half-Yki. Yki paws are adapted for travel over slick and cold surfaces; their paw-pads have ‘treads’, raised ridges that are unique to each individual. Yki claws are long and hook-like, perfect for snaring a meal or gripping slippery ice. Between their toes grows long, course hair that protects the feet from the elements. The lower portion of their legs also has longer fur, although it is the same fur that is found all over the body.\n\nIt has been found that Yki introduced to warmer climates will moult their outer coat, leaving only the incredibly thick and luxurious undercoat. When reintroduced to their homelands, the Yki will re-grow the outer coat within a matter of days.\n\nThe Yki always have white coats, with a secondary color for markings, hair, and tail flame (in males). Occasionally a male will be born with a black base instead of white, but this is a rare occurrence; it happens no more than 1 in 100 births. If a single kit in a litter bears a black coat, chances are it's litter-mates will as well. The only exception to the white/black base rule is half-Yki, who's pelt colour may be affected by their non-Yki parent.\n\nThere is a particular hereditary gene found in a few Yki families, particularity the Jori and Tuggheja clans. The gene is recessive, and carried by the female, although it only seems to manifest itself in males. It affects the Yki's secondary colour, reversing the pelts colors so that the secondary colour overwhelms the white base. To all appearances the affected Yki seems to be a reverse of a normal individual, with white markings on a colour base instead of the opposite.\n\nWings are a common trait amongst the Yki, but only feathered wings are seen. Scaled or bat-like wings (thin skin covered by short fur) are unsuitable for the arctic environment they inhabit. Half-Yki may occasionally defy this rule, but it's rare for them to survive on their own, depending on their family; as the amount of exposed skin on their wings can prove hazardous to their health, and often fatal.\n\nTribes identify each other by facial tattoos, given when a kit turns five. These tattoos are unique to each tribe, and are added to as the Yki matures; given in recognition of specific events, much like the grading process in use in other parts of the world. A few of the more southern tribes grow out their fur and hair and wear it in dreadlocks, and then adored with beads and other ornaments made of coloured stones or metal."


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
