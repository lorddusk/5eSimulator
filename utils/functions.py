class AbilityScores:
    def __init__(self, name: str, str_: int, dex: int, con: int, int_: int, wis: int, cha: int):
        self.strength = str_
        self.dexterity = dex
        self.constitution = con
        self.intelligence = int_
        self.wisdom = wis
        self.charisma = cha
        self.name = name

    def get_mod(self, stat):
        return {'str': self.strength // 2 - 5, 'dex': self.dexterity // 2 - 5,
                'con': self.constitution // 2 - 5, 'int': self.intelligence // 2 - 5,
                'wis': self.wisdom // 2 - 5, 'cha': self.charisma // 2 - 5}.get(stat, 0)

class Attacks:
    def __init__(self, data):
        self.name = data['name']
        self.hit = data.get('hit',0)
        self.dc = data.get('dc',0)
        self.save = data.get('save','')
        self.half = data.get('half', False)
        self.damage = data['damage']

class SimStats:
    def __init__(self):
        self.attacks = 0
        self.attacksHit = 0
        self.attacksMiss = 0
        self.defends = 0
        self.defendsSuccess = 0
        self.defendsFailed = 0
        self.damageDealt = 0
        self.damageTaken = 0

    def get_stats(self):
        return f"Attacks: {self.attacks}\n\tHits: {self.attacksHit}\n\tMisses: {self.attacksMiss}\n" \
            f"Defends: {self.defends}\n\tSuccesses: {self.defendsSuccess}\n\tFailures: {self.defendsFailed}\n" \
            f"Damage Dealt: {self.damageDealt}\n" \
            f"Damage Taken: {self.damageTaken}"
