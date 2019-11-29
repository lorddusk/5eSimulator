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
