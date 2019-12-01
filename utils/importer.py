import json

from models.player import Player


def importEnemies():
    file = json.load(open("./simulationfiles/enemies.json", "r"))
    return [Player.from_data(r) for r in file]


def importPlayers():
    file = json.load(open("./simulationfiles/players.json", "r"))
    return [Player.from_data(r) for r in file]
