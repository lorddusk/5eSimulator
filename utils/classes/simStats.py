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