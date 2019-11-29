import json

import config
from utils.dice import roll
from models.player import Player
import collections
import random

def importEnemies():
    file = json.load(open("./simulationfiles/enemies.json", "r"))
    return [Player.from_data(r) for r in file]


def importPlayers():
    file = json.load(open("./simulationfiles/players.json", "r"))
    return [Player.from_data(r) for r in file]


def rollInitiative(enemyList, playerList):
    for x in playerList:
        init = roll(f"1d20+{x.get_mod('dexterityMod')}")
        x.initiative = init.plain
    for x in enemyList:
        init = roll(f"1d20+{x.get_mod('dexterityMod')}")
        x.initiative = init.plain

def debug(text):
    if printing:
        print(text)

def line():
    print("---------------------------")

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
                attack = random.choice(x.attacks)
                debug(f"\t{x.name} attacking: {enemy.name} with {attack.name}")
                if attack.hit is not 0:
                    atk = roll(f"1d20+{attack.hit}")
                    if atk.plain >= enemy.ac:
                        x.simStats.attacksHit += 1
                        enemy.simStats.defendsFailed += 1
                        damage = roll(attack.damage)
                        enemy.hp = enemy.hp - damage.plain
                        x.simStats.damageDealt += damage.plain
                        enemy.simStats.damageTaken += damage.plain
                        debug(f"\t\tHit! (did {damage.plain} damage)")
                        debug(f"\t\t{enemy.name} has {enemy.hp} HP left.")
                    else:
                        x.simStats.attacksMiss += 1
                        enemy.simStats.defendsSuccess += 1
                        debug("\t\tMiss!")
                else:
                    save = roll(f"1d20+{enemy.get_mod('dexterityMod')}")
                    if save.plain >= attack.dc:
                        x.simStats.attacksHit += 1
                        enemy.simStats.defendsFailed += 1
                        damage = roll(attack.damage)
                        enemy.hp = enemy.hp - damage.plain
                        x.simStats.damageDealt += damage.plain
                        enemy.simStats.damageTaken += damage.plain
                        debug(f"\t\tFailed Saving Throw! (did {damage.plain} damage)")
                        debug(f"\t\t{enemy.name} has {enemy.hp} HP left.")
                    else:
                        x.simStats.attacksMiss += 1
                        enemy.simStats.defendsSuccess += 1
                        debug("\t\tSaved Saving Throw!")
                if enemy.hp <= 0:
                    debug(f"\t\t\t{enemy.name} died!")
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
        debug("---------------------------")
        i = i + 1
    debug("---------------------------")
    if playersAlive == 0:
        debug("Enemies Won!")
        FightStats(everyone)
        return 1
    if enemiesAlive == 0:
        debug("Players Won!")
        FightStats(everyone)
        return 0


def FightStats(everyone):
    debug("---------------------------")
    debug(f"----Overall Statistics----")
    for y in everyone:
        debug(y.name)
        debug(y.simStats.get_stats())
        debug("---------------------------")


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
        debug("-------------------------")
        if reports != 0:
            if i % reports == 0:
                print(f"Progress after {reports} fights (total {i}):")
                print(f"\tPlayers won {playerSim} times")
                print(f"\tEnemies won {enemySim} times\n")
                playerSim = 0
                enemySim = 0
    print(f"End result after {amount} fights:")
    print(f"\tPlayers won {playerWins} out of {amount} times")
    print(f"\tEnemies won {enemyWins} out of {amount} times")

amount = config.amount
reports = config.reports
printing = config.debug

run()
