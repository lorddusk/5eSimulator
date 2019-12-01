from main import line, debug


def FightStats(everyone):
    line()
    debug(f"----Overall Statistics----")
    for y in everyone:
        debug(y.name)
        debug(y.simStats.get_stats())
        line()


def checkAttackType(attack, enemy, x):
    if attack.type == "MA" or attack.type == "RA":
        debug(f"\t\t{x.name} attacking {enemy.name} with a {attack.name}")
    if attack.type == "MS" or attack.type == "RS":
        debug(f"\t\t{x.name} casting {attack.name}.\n\t\tTarget: {enemy.name}")
