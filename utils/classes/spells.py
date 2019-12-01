from utils.classes.effects import AttackEffect


class Spells:
    def __init__(self, spells):
        self.spells = spells


class SpellLevel:
    def __init__(self, slots, spells):
        self.slots = slots
        self.spells = spells


class Spell:
    def __init__(self, data):
        self.name = data['name']
        self.hit = data.get('hit', None)
        self.dc = data.get('dc', None)
        self.save = data.get('save', None)
        self.half = data.get('half', False)
        self.damage = data['damage']
        self.type = data['type']
        if data.get('effect') is not None:
            effect = data.get('effect').split(",")
            self.effect = AttackEffect(effect[0],effect[1],int(effect[2]),effect[3])
        else:
            self.effect = None