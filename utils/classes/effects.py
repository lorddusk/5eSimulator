class AttackEffect:
    def __init__(self, who, effect, duration, what):
        self.who = who
        self.effect = effect
        self.duration = duration
        self.what = what


class Effect:
    def __init__(self, effect, duration, what):
        self.effect = effect
        self.duration = duration
        self.what = what