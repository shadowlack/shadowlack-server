class Races():
    def __init__(self):
        self.name = None
        self.plural_name = None
        self.scientific_name = None

        # race-specific
        self.languages = {}
        self.has_mutations = False
        self.is_playable = True
        self.homeworld = "Ramath-lehi"
        self.can_interbreed = True

        self.help_text = None
        self.h_perc = 0.00

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
        self.plural_name = "Anubi"
        self.scientific_name = "draco sapiens anubidis"
        self.min_height = 1.70
        self.max_height = 2.23
        self.min_weight = 38.56
        self.max_weight = 81.65
        self.languages = {"Odyre"}
        # bonus lore, biotech


class Aquabat(Races):
    def __init__(self):
        super().__init__()
        self.name = "Aquabat"
        self.plural_name = "Aquabats"
        self.scientific_name = "resaquatilis sapiens"
        self.min_height = 1.65
        self.max_height = 2.00
        self.min_weight = 38.56
        self.max_weight = 72.57
        # bonus athletics, notice
        # can change gender
        # can breathe underwater
        self.can_interbreed = False


class Feydragon(Races):
    def __init__(self):
        super().__init__()
        self.name = "Feydragon"
        self.plural_name = "Feydragons"
        self.scientific_name = "draco sapiens pauxillulus"
        self.min_height = 0.69
        self.max_height = 1.10
        self.min_weight = 6.80
        self.max_weight = 27.00
        # bonus fronima, empathy
        self.has_mutations = True


class Khell(Races):
    def __init__(self):
        super().__init__()
        self.name = "Khell"
        self.plural_name = "Khellin"
        self.scientific_name = "draco sapiens terragelatum"
        self.min_height = 1.80
        self.max_height = 2.40
        self.min_weight = 150.00
        self.max_weight = 250.00
        self.languages = {"Khellakh"}
        # bonus technology, fight
        # penalty in warm places (heavy insulating fur)


class Lukuo(Races):
    def __init__(self):
        super().__init__()
        self.name = "Lukuo"
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
        self.plural_name = "Pendragons"
        self.scientific_name = "draco sapiens"
        self.min_height = 1.65
        self.max_height = 2.18
        self.min_weight = 45.35
        self.max_weight = 158.76
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
        # bonus artistry, deceive
