Points will be loosely based on DnD rules, but that won't be apparent to the user.

Starting Health

# Constants
* Life Support Decay = 15
* Fire Suppression = 2
* Base Warp Threshold = For starting battle, will be disabled
* Station Fire Chance = 0
* Station Damage Chance = 0

# Player
* MAX/Hull Health = 100
* MAX/Life Support = 100
* Accuracy = 4

## Player Stations

### Auto Turret
* Attack Power = 5
* Boost = 5
### Cockpit
* Dodge = 2
* Boost = 1
### Life Support
* Life Support Charge = 15
* Boost = 15

# Opponent 1 - Damaged Destroyer

* MAX/Hull Health = 50
* Attack Power = 5
* Shields = 0
* Dodge = 2
* Accuracy = 4


# Mock Combat

## Round 1
* Move C1 to AT
* Move C2 to C
* GO
* Player
  * P + 5
  * D + 2
  * LS = 100
  * HH = 100
* Enemy
  * HH = 50
* Player -> Enemy:
  * A(4) -> eD(2) -> 50% chance
  * Hit
  * P(5+5) - S(0) -> eHH(50) - 10 -> HH(40)
* Enemy -> Player
  * eA(4) -> D(2 + 1) -> 25% chance
  * HIt
  * eP(5) - S(0) -> HH(100) - 5 -> HH(95)
  * Damage C
## Round 2
* GO
* Player
  * P + 5
  * ~D
  * LS = 100
  * HH = 95
* Enemy
  * HH = 40
* Player -> Enemy:
  * A(4) -> eD(2) -> 50% chance
  * Miss
* Enemy -> Player
  * eA(4) -> D(0) -> 100% chance
  * Hit
  * eP(5) - S(0) -> H(95) - 5 -> HH(90)
  * Fire LS
* Repaired C
## Round 3
* Move C1 to LS (from AT)
* GO
* Player
  * D + 1
  * LS (F)
  * LS = 100
  * HH = 90
* Enemy
  * HH = 40
* Player -> Enemy:
  * A(4) -> eD(2) -> 50% chance
  * Hit
  * P(5) - S(0) -> eHH(40) - 5 -> HH(35)
* Enemy -> Player
  * eA(4) -> D(2 + 1) -> 25% chance
  * Miss
* Suppress Fire in LS
## Round 4
* Move C1 to C
* GO
* Player
  * P + 5
  * D + 1
  * LS = 100
  * HH = 90
* Enemy
  * HH = 35
* Player -> Enemy:
  * A(4) -> eD(2) -> 50% chance
  * Miss
* Enemy -> Player
  * eA(4) -> D(2 + 1) -> 25% chance
  * Hit
  * eP(5) - S(0) -> HH(90) - 5 -> HH(85)
  * Damage LS
## Round 5
* Move C2 to LS (from C)
* GO
* Player
  * P + 5
  * D
  * LS (D)
  * LS = 100
  * HH = 85
* Enemy
  * HH = 35
* Player -> Enemy:
  * A(4) -> eD(2) -> 50% chance
  * Hit
  * P(5+5) - eS(0) -> eHH(35) - 10 -> eHH(25)
* Enemy -> Player
  * eA(4) -> D(2) -> 50% chance
  * Hit
  * eP(5) - S(0) -> HH(85) - 5 -> HH(80)
* LS(100) - LSD(15) -> LS(85)
* Repaired LS
## Round 6
* Move C2 to AT (from LS)
* GO
* Player
  * P + 5
  * D + 1
  * LS = 85
  * HH = 80
* Enemy
  * HH = 25
* Player -> Enemy:
  * A(4) -> eD(2) -> 50% chance
  * Miss
* Enemy -> Player
  * eA(4) -> D(2 + 1) -> 25% chance
  * Miss
## Round 7
* GO
* Player
  * P + 5
  * D + 1
  * LS = 85
  * HH = 80
* Enemy
  * HH = 25
* Player -> Enemy:
  * A(4) -> eD(2) -> 50% chance
  * Hit
  * P(5+5) - eS(0) -> eHH(25) - 10 -> eHH(15)
* Enemy -> Player
  * eA(4) -> D(2 + 1) -> 25% chance
  * Hit
  * eP(5) - S(0) -> HH(80) - 5 -> HH(75)
  * Damage C
## Round 8
* GO
* Player
  * P + 5
  * D (D)
  * LS = 85
  * HH = 75
* Enemy
  * HH = 15
* Player -> Enemy:
  * A(4) -> eD(2) -> 50% chance
  * Miss
* Enemy -> Player
  * eA(4) -> D(2) -> 50% chance
  * Hit
  * eP(5) - S(0) -> HH(75) - 5 -> HH(70)
  * Damage C
* Repair C (but it was damaged again)
## Round 9
* GO
* Player
  * P + 5
  * D (D)
  * LS = 85
  * HH = 70
* Enemy
  * HH = 15
* Player -> Enemy:
  * A(4) -> eD(2) -> 50% chance
  * Hit
  * P(5+5) - eS(0) -> eHH(15) - 10 -> eHH(5)
* Enemy -> Player
  * eA(4) -> D(2) -> 50% chance
  * Miss
* Repair C
## Round 10
* GO
* Player
  * P + 5
  * D + 1
  * LS = 85
  * HH = 70
* Enemy
  * HH = 5
* Player -> Enemy:
  * A(4) -> eD(2) -> 50% chance
  * Miss
* Enemy -> Player
  * eA(4) -> D(2+1) -> 25% chance
  * Miss
## Round 11
* GO
* Player
  * P + 5
  * D + 1
  * LS = 85
  * HH = 70
* Enemy
  * HH = 5
* Player -> Enemy:
  * A(4) -> eD(2) -> 50% chance
  * Hit
  * P(5+5) - eS(0) -> eHH(5) - 10 -> eHH(0)
* Enemy -> Player
  * eA(4) -> D(2+1) -> 25% chance
  * Hit
  * eP(5) - S(0) -> HH(70) - 5 -> HH(65)
  * Fire LS
* END GAME: Opponent Hull Destroyed
