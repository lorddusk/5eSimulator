import logging

from utils.classes.abilityScores import AbilityScores
from utils.classes.attacks import Attacks
from utils.classes.simStats import SimStats

log = logging.getLogger(__name__)

class Player:
    def __init__(self, name: str, ac: int, hp: int, ability_scores: AbilityScores, type: str, prof: int, noa: int, attacks: Attacks, simStats: SimStats, saves):
        self.name = name
        self.hp = hp
        self.ac = ac
        self.strength = ability_scores.strength
        self.dexterity = ability_scores.dexterity
        self.constitution = ability_scores.constitution
        self.intelligence = ability_scores.intelligence
        self.wisdom = ability_scores.wisdom
        self.charisma = ability_scores.charisma
        self.prof = prof
        self.noa = noa
        self.attacks = attacks
        self.type = type
        self.simStats = simStats
        self.saves = saves
        self.effects = []
        self.initiative = 0

    @classmethod
    def from_data(cls, data):
        ac = data['ac']
        hp = data['hp']
        type = data['type']
        prof = data['prof']
        noa = data['noa']
        attacks = []
        for attack in data['attacks']:
            try:
                x = Attacks(attack)
                attacks.append(x)
            except Exception as e:
                log.error(e)
        try:
            scores = AbilityScores(data['name'], data['str'] or 10, data['dex'] or 10, data['con'] or 10, data['int'] or 10,
                                   data['wis'] or 10, data['cha'] or 10)
        except Exception as e:
            log.error(e)
        saves = []
        for save in data['saves']:
            try:
                saves.append(save)
            except Exception as e:
                log.error(e)

        return cls(data['name'], ac, hp, scores, type, prof, noa, attacks, SimStats(), saves)

    def get_stat_array(self):
        """
        Returns a string describing the monster's 6 core stats, with modifiers.
        """
        str_mod = self.strength // 2 - 5
        dex_mod = self.dexterity // 2 - 5
        con_mod = self.constitution // 2 - 5
        int_mod = self.intelligence // 2 - 5
        wis_mod = self.wisdom // 2 - 5
        cha_mod = self.charisma // 2 - 5
        return f"**STR**: {self.strength} ({str_mod:+}) **DEX**: {self.dexterity} ({dex_mod:+}) " \
               f"**CON**: {self.constitution} ({con_mod:+})\n**INT**: {self.intelligence} ({int_mod:+}) " \
               f"**WIS**: {self.wisdom} ({wis_mod:+}) **CHA**: {self.charisma} ({cha_mod:+})"

    def get_mod(self, stat):
        """
        Gets the monster's stat modifier for a core stat.
        :param stat: The core stat to get. Can be of the form "cha", "charisma", or "charismaMod".
        :return: The monster's relevant stat modifier.
        """
        valid = ["strengthMod", "dexterityMod", "constitutionMod", "intelligenceMod", "wisdomMod", "charismaMod"]
        stat = next((s for s in valid if stat in s), None)
        if stat is None:
            raise ValueError(f"{stat} is not a valid stat.")
        score = (self.strength, self.dexterity, self.constitution, self.intelligence, self.wisdom, self.charisma)[
            valid.index(stat)]
        return score // 2 - 5