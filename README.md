# 5eSimulator
Simulates combat between parties and their encounters, with the 5th edition ruleset.

# Current Status
- The "AI" is incredibly stupid, it randomly selects a target, without checking for range or current health.
- Spells/attacks with saving throws are always "Save or Suck".
- Iniative is rolled, but not used.
- Attacks are always within range. (5ft for melee, 10ft for ranged)
- Area of Effect is single target
- Proficiency in saving throws is not implemented (what I did is increase the stat modifier by whatever the save prof would be. so a +4 would increase the stat with 8, etc.)


# ToDo in order of randomization
[ ] Actually use iniative
[ ] "Smart" selecting of targets
[ ] Implement "Save and Half" damage for spells/attacks with saving throws
[ ] Make AoE multi target
[ ] Save Profiency support
