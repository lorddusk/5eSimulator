import random

import math

import config
from utils.classes.effects import Effect
from utils.debug import FightStats, checkAttackType
from utils.dice import roll
from utils.importer import importEnemies, importPlayers


def debug(text):
    if debugPrint:
        print(text)


def line():
    debug("---------------------------")


def rollInitiative(enemyList, playerList):
    for x in playerList:
        init = roll(f"1d20+{x.get_mod('dexterityMod')}")
        x.initiative = init.plain
    for x in enemyList:
        init = roll(f"1d20+{x.get_mod('dexterityMod')}")
        x.initiative = init.plain


def combat(enemyList, playerList):
    debug("Rolling Initiative...")
    rollInitiative(enemyList, playerList)
    enemiesAlive = len(enemyList)
    playersAlive = len(playerList)
    contenders = playerList + enemyList
    contenders.sort(key=lambda i: i.initiative, reverse=True)
    everyone = playerList + enemyList
    i = 1
    fight = True
    while fight:
        debug(f"Round {i} ({len(contenders)} contenders left):")
        for x in contenders:
            if len(enemyList) >= 1 and len(playerList) >= 1:
                debug(f"\t{x.name}:")
            else:
                fight = False
                continue
            for attacks in range(x.noa):
                x.simStats.attacks += 1
                if x.type == "p":
                    if len(enemyList) >= 1:
                        enemy = random.choice(enemyList)
                        enemy.simStats.defends += 1
                    else:
                        fight = False
                        continue
                elif x.type == "e":
                    if len(playerList) >= 1:
                        enemy = random.choice(playerList)
                        enemy.simStats.defends += 1
                    else:
                        fight = False
                        continue
                selectAndExecute(enemy, x)
                if enemy.hp <= 0:
                    debug(f"\t\t\t\t{enemy.name} died!")
                    if enemy.type == "p":
                        playerList.remove(enemy)
                        contenders.remove(enemy)
                        playersAlive = len(playerList)
                        if playersAlive == 0:
                            fight = False
                            continue
                    elif enemy.type == "e":
                        enemyList.remove(enemy)
                        contenders.remove(enemy)
                        enemiesAlive = len(enemyList)
                        if enemiesAlive == 0:
                            fight = False
                            continue
        line()
        i = i + 1
    line()
    if playersAlive == 0:
        debug("Enemies Won!")
        if stats:
            FightStats(everyone)
        return 1
    if enemiesAlive == 0:
        debug("Players Won!")
        if stats:
            FightStats(everyone)
        return 0


def selectAndExecute(enemy, x):
    if x.spells is not None:
        atsp = random.randint(1, 2)
    else:
        atsp = 1
    if atsp == 1:
        attack = random.choice(x.attacks)
        checkAttackType(attack, enemy, x)
        executeAttack(attack, enemy, x)
    elif atsp == 2:
        spells = random.choice(x.spells)
        slots = spells.slots
        if slots is None and not 0:
            attack = random.choice(spells.spells)
            checkAttackType(attack, enemy, x)
            executeAttack(attack, enemy, x)
        else:
            if spells.slots == 0:
                selectAndExecute(enemy, x)
            else:
                attack = random.choice(spells.spells)
                checkAttackType(attack, enemy, x)
                executeAttack(attack, enemy, x)
                spells.slots -= 1
                print(f"{spells.slots} Spell Slots remaining.")


def executeAttack(attack, enemy, x):
    if attack.hit is not None:
        atk = checkForAttackEffect(attack, enemy)
        if atk.plain >= enemy.ac:
            attackHit(atk, attack, enemy, x)
        else:
            attackMiss(atk, enemy, x)
        applyEffect(attack, enemy)
    else:
        mod = getSaveMod(attack, enemy)
        save = roll(f"1d20+{mod}")
        if save.plain < attack.dc:
            saveFailure(save, attack, enemy, x)
            applyEffect(attack, enemy)
        else:
            if attack.half:
                saveFailure(save, attack, enemy, x)
            else:
                saveSuccess(attack, enemy, save, x)


def getSaveMod(attack, enemy):
    if attack.save in enemy.saves:
        mod = enemy.get_mod(attack.save) + enemy.prof
    else:
        mod = enemy.get_mod(attack.save)
    return mod


def processEffect(effect):
    effect.duration -= 1
    return effect


def checkForAttackEffect(attack, enemy):
    if len(enemy.effects) > 0:
        for f in enemy.effects:
            if f.what.lower() == "attack":
                f = processEffect(f)
                atk = roll(f"1d20+{attack.hit} {f.effect.lower()}")
                if f.duration == 0:
                    enemy.effects.remove(f)
            else:
                atk = roll(f"1d20+{attack.hit}")
    else:
        atk = roll(f"1d20+{attack.hit}")
    return atk


def saveSuccess(attack, enemy, save, x):
    x.simStats.attacksMiss += 1
    enemy.simStats.defendsSuccess += 1
    debug(f"\t\t\t{enemy.name} rolled {save.plain}, DC is {attack.dc}")
    debug("\t\t\t\tSucceeded Saving Throw!")


def attackMiss(atk, enemy, x):
    x.simStats.attacksMiss += 1
    enemy.simStats.defendsSuccess += 1
    if "disadv" in atk.result:
        debug(f"\t\t\tRolled {atk.plain} with disadvantage, AC is {enemy.ac}")
    else:
        debug(f"\t\t\tRolled {atk.plain}, AC is {enemy.ac}")
    debug("\t\t\t\tMiss!")


def saveFailure(save, attack, enemy, x):
    damage = roll(attack.damage)
    debug(f"\t\t\tRolled a {save.plain}, DC is {attack.dc}")
    if not attack.half:
        debug(f"\t\t\t\tFailed Saving Throw! (did {damage.plain} damage)")
        enemy.hp = enemy.hp - damage.plain
        x.simStats.damageDealt += damage.plain
        enemy.simStats.damageTaken += damage.plain
        x.simStats.attacksHit += 1
        enemy.simStats.defendsFailed += 1
    else:
        halved = math.floor((damage.plain / 2))
        debug(f"\t\t\t\tSucceeded Saving Throw! Only took half damage. (did {halved} damage)")
        enemy.hp = enemy.hp - halved
        x.simStats.damageDealt += halved
        enemy.simStats.damageTaken += halved
        x.simStats.attacksMiss += 1
        enemy.simStats.defendsSuccess += 1

    debug(f"\t\t\t\t{enemy.name} has {enemy.hp} HP left.")


def attackHit(atk, attack, enemy, x):
    x.simStats.attacksHit += 1
    enemy.simStats.defendsFailed += 1
    damage = roll(attack.damage)
    enemy.hp = enemy.hp - damage.plain
    x.simStats.damageDealt += damage.plain
    enemy.simStats.damageTaken += damage.plain
    if "disadv" in atk.result:
        debug(f"\t\t\tRolled {atk.plain} with disadvantage, AC is {enemy.ac}")
    else:
        debug(f"\t\t\tRolled {atk.plain}, AC is {enemy.ac}")
    debug(f"\t\t\t\tHit! (did {damage.plain} damage)")
    debug(f"\t\t\t\t{enemy.name} has {enemy.hp} HP left.")


def applyEffect(attack, enemy):
    if attack.effect is not None:
        if attack.effect.who == "target":
            enemy.effects.append(
                Effect(attack.effect.effect, int(attack.effect.duration), attack.effect.what))


def run():
    playerWins = 0
    enemyWins = 0
    playerSim = 0
    enemySim = 0
    print(f"Simulating {amount} fights...")
    for i in range(1, (amount + 1)):
        debug(f"Simulation {i} out of {amount}")
        enemies = importEnemies()
        players = importPlayers()
        win = combat(enemies, players)
        if win == 0:
            playerWins += 1
            playerSim += 1
        elif win == 1:
            enemyWins += 1
            enemySim += 1
        line()
        if reports != 0:
            if i % reports == 0:
                print(f"Progress after {reports} fights (total {i}):")
                print(f"\tPlayers won {playerSim} times")
                print(f"\tEnemies won {enemySim} times\n")
                playerSim = 0
                enemySim = 0
    line()
    print(f"End result after {amount} fights:")
    print(f"\tPlayers won {playerWins} times ({calcPercentage(playerWins, amount)}%)")
    print(f"\tEnemies won {enemyWins} times ({calcPercentage(enemyWins, amount)}%)")


amount = config.amount
reports = config.reports
debugPrint = config.debug
stats = config.stats


def calcPercentage(x, y):
    if not x and not y:
        return None
    elif x < 0 or y < 0:
        return None
    else:
        return 100 * float(x) / float(y)


run()
