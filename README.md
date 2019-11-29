# 5eSimulator
Simulates combat between parties and their encounters, with the 5th edition ruleset.

# Current Status
- The "AI" is incredibly stupid, it randomly selects a target, without checking for range or current health.
- The "AI" also selects a random attack out of their arsenal.
- Spells/attacks with saving throws are always "Save or Suck".
- Iniative is rolled, but not used.
- Attacks are always within range. (5ft for melee, 10ft for ranged)
- Area of Effect is single target
- Proficiency in saving throws is not implemented (what I did is increase the stat modifier by whatever the save prof would be. so a +4 would increase the stat with 8, etc.)

# How to run
You will need python 3.7, and just run the main.py file.

Changing the settings can be done in the config.py file.

Your "players" need to be in a file called players.json in /simulationfiles

Your "enemeies" need to be in a file called enemies.json in /simulationfiles

# ToDo in order of randomization
- [x] Actually use iniative
- [ ] Weight system for attacks
- [ ] Recharge system for Rechargable effects
- [ ] "Smart" selecting of targets
- [x] Implement "Save and Half" damage for spells/attacks with saving throws
- [ ] Make AoE multi target
- [x] Save Proficiency support
- [ ] Implement racial abilities
- [ ] Implement class abilities
- [ ] Support for healing spells
- [ ] Support for buff spells
- [ ] Support for not-buff spells (Fear for example)
