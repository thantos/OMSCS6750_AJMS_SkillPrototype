# Quick Particle Overview

## Stats

### Combat

* Accuracy (A)
  * Chance to hit
  * Station: Targeting Computer
  * Base Value: >0
  * Range: 0 > x
  * Explanation: a value of 1 is 100% chance to hit enemy with no dodge See Logic section for more info.
* Attack Power (P)
  * Damage which is done.
  * Station: Auto Turret
  * Base Value: 0
  * Range: ?
* Dodge (D) (?)
  * Ability to avoid enemy fire
  * Station: Cockpit
  * Base Value: 0
  * Range: 0 >= x
  * Explanation: a value of 1 is 100% chance to dodge an enemy attack with accuracy < 1. See Logic section for more info.
* Shield (S)
  * Absorbs damage
  * Station: Shield
  * Base Value: 0
  * Range: ?

### Escape

* Warp (W)
  * Impacts time to run away
  * Station: Engines, Cockpit
  * Base Value: 0
  * Range: ?
* Intercept (I)
  * Ability to stop enemy from warping
  * Station: Tractor Beam
  * Base Value: 0
  * Range: ?

### Ship
* Life Support (LS)
  * Current life support value, crew dies at 0.
  * Station: Life Support
  * Base Value: MLS
  * Range: ?
* Life Support Charge (LSC)
  * Amount life support increases each round (up to MLS)
  * Station: Life Support
  * Base Value: 0
  * Range: ?
* Max Life Support (MLS)
  * Max value life support can be charged to.
  * Station: Life Support  
  * Base Value: MIN(Range)
  * Range: ?
* Hull Health (H)
  * Current hull health.
  * Station: Maintenance
  * Base Value: MH
  * Range: ?
* Max Hull Health (MH)
  * Max value for hull health.
  * Station: Maintenance
  * Base Value: MIN(Range)
  * Range: ?

## Constants

### Fire Suppression (FS)
* Base Value: 1

### Station Fire Chance (SFC)
* Base Value: ?

### Station Damage Chance (SDC)
* Base Value: ?

### Life Support Decay (LSD)
* Base Value: ?

### Base Warp Level (BWL)
* Base Value: > 0

## Stations

### Life Support

Keeps crew alive

* Working: Provides X to LS.
* Manned: Provides additional X% to LS.
* Damaged: Provides nothing. (LS will decrease by LSD)

### Cockpit

* Working: Provides X to D.
* Manned: Provides additional D by X%.
* Damaged: Provides nothing. Cannot Warp.

### Auto Turret

* Working: Provides X to P.
* Manned: Provides additional P by X%.
* Damaged: Provides nothing.

### Targeting Computer

* Working: Provides X to A.
* Manned: Provides additional A by X%.
* Damaged: Provides nothing.

### Shields

* Working: Provides X S.
* Manned: Provides additional S by X%.
* Damaged: Provides nothing.

### Engines

* Working: Provides X W/turn.
* Manned: Provides additional X% W/turn.
* Damaged: Provides nothing. Cannot Warp.

### Tractor Beam

* Working: Provides X I.
* Manned: Provides additional X% I.
* Damaged: Provides nothing.

### Maintenance

* Working: Provides X M.
* Manned: Provides additional X M.
* Damaged: Provides nothing.

## Game Loop

1. Report Current State
1. Player Commands Crew.
1. Update Stats based on new Position
1. Combat
1. Apply Tasks
  1. Repair/Fire Suppression
1. Apply Combat Impacts
1. Check for End Game States
1. Repeat @ 1

### Summary

Report the current state to the player, this includes the state of room (on fire, in need of repair), positions of crew members, state of the hull, state of life support, state of the enemy, result of combat (Note: we should write logic to reduce the quantity of data that is reported each round).

The player is now given the ability to command the crew.

Now we calculate the new ship states based on the location of the crew and the state of the stations.

We calculate combat based on the current ship stats.

We apply room repairs.

We apply combat results, damaged stations, fires, hull damage, etc.

we check for end game states (hull damage, life support).

Go back to the start where we report the current state.

## Logic

### Combat
Each round ends with combat between the two ships.

Hit chance will be calculated between 0 and 1. If the different between accuracy and dodge (A-eD) is greater or equal to 1, there is a 100% chance to hit. If the different is less than 0, the chance is 0.

#### Logic
* if A > 0 and P > 0
  * HIT % = (A - eD)%
  * if HIT
    * Damage = P - eS
    * if Damage > 0
      * For Random Station (This should not be random in the future)
        * Start Station Fire Chance = (SFC)%
        * Station Damaged Chance = (SDC)%

### Station State
Each round a station may be manned or unmanned, on fire or not on fire, and damaged or undamaged. Being manned will start to clear up any negative issues, eventually resulting in a boost. Unmanned will keep negative effect, only producing benefits when clear of fire or damage.

#### Logic
* If station.manned
  * if station.fire > 0
    * remove Fire
  * elif station.damaged
    * remove Damaged
  * else
    * Apply Manned Boost
* else
  * if station.fire
    * station.fire += 1
  * if station.fire > FS (fire Suppression)
    * Add Damaged
  * elif station.damaged
    * skip station
  * else
    * Normal Operation


### Life Support
Life support keeps the crew alive. Even when life support is damaged, the ship can maintain life, but only for a limited time. Each round the life support reduced based on the LSD (life support decay). The decay can be counteracted by the life support module's LSC (life support charge) output. The life support module is damaged, life support (LS) will eventually decay to 0, at which point the crew dies.

### Escape
Ship can try to escape battle when damaged or uninterested in combat. First they must change their W (Warp) to the BWL (base warp level). After that they can warp, unless the enemy has some level of (I) intercept, generally from a tractor beam. To escape, W must be greater than the sum of the base warp level and the enemy's intercept (BWL + eI).

#### Logic
* Escape = B > (BWL + eI)

## Cause and Effect Reporting

An interesting addition would be to make the combat/advancement report interesting. Consider, why did was the ship able to dodge an attack, why were the shields boosted. (Generally because of the crew boosting rooms). We could compare used in calculating game state with the values if the room was or wasn't boosted.

"The attack was avoided due to Lester's quick thinking in the cockpit."
"The enemy was critically damaged due to Lester's Quick Thinking in the Auto Turret."

Or Negative events:

* "Major damage taken, repairing the shields is of the upmost importance."
* "We are being hit, I think that a talented captain could avoid these impacts."
* "Losing life support is damaged, we need it to be repaired."

And general maintenance updates may be required, like:

* "Lester has repaired the Cockpit"
* "The fire has been extinguished by Lester"

Might consider ranking both positive and negative events by the number of turns it would take to succeed/fail. This won't work for something like dodging, completely missing or not being missed doesn't accumulate. This leads to two categories of effects.

Passive - Does or doesn't have an impact, might not be possible to hit without a manned targeting computer:
* Dodge
* Accuracy
* Intercept

Cumulative - Will this cause lead to more success or failure, life support will fail in X turns, X turns of extra damage will lead to success:
* Life Support Charge
* Attack Power
* Shields
* Hull Health
* Warp

Another purpose will be report unnecessary manned station:

* "Captain, we are far out maneuvering the enemy's attempts to avoid our attacks." (Overpowering Dodge)
* "Life support is fully charged, Lester would be more effective elsewhere." (Don't need life support charge)
* "Hull to repaired and stable. Lester is looking to be useful elsewhere." (No need for hull maintenance, or the hull is fully repaired while maintenance is manned)

### Negative Levels
#### Impossible
It is not possible to do this action.

* Shields - Their attacks overpower the shields no matter the level (Or does this fall into the unnecessary category?)
* Attack Power - No amount of crew support will improve the attack power to a point where our attacks will bypass their shields.
* Dodge - We cannot dodge their attacks, their accuracy exceeds our ability to dodge
* Accuracy - We cannot hit them, no matter if we are manned or not

#### Repair Required Imminent
When repairing is the only way to stay alive, maybe without maintenance we will (can?) lose remaining hull health next turn. This would be for some value X (2?).


#### Manning Required Imminent
Manning a station could keep us from losing in X turns.

#### Fire Suppression Suggested

### Negative Action

#### Levels
##### Imminent Need
When [repairing|manning|fire supression] is the only way to stay alive, maybe without maintenance we will (can?) lose remaining hull health next turn. This would be for some value X (2?). Only for cumulative effects.

* Hull Health - If maintenance isn't [Action], the enemy could destroy us in X turns
* Shield - If the shields are not [Action], the damage taken will be fatal in X turns
* Life Support - If life support isn't [Action], will lose in X turns.
* Intercept - With no tractor beam, the enemy will escape in X turns.

##### Suggested Need
Cumulative: Like imminent but greater than X. Passive: Without [Action] intended effect cannot be done.
##### Wasteful
##### Unnecessary

#### Actions
##### Repair Station
##### Man Station
##### Suppress Fire

#### Effect Levels
##### Necessary
##### Important
##### Trivial

#### Effects
##### Dodging or Absorbing Attacks
***Important***

The need to avoid or absorb attacks is import. Damage can be taken for a while, but eventually it will start causing an imminent situation.
##### Hitting and Causing Damage or Warping
***Necessary***

If we cannot find a way to cause damage or warp, why even try.
##### Can Intercept/Intercepting
***Important***

We likely want to stop the enemy from fleeing.
##### Maintain Life Support
***Necessary***

If we cannot maintain life support, we don't keep on living.
##### Maintain Hull Health
***Necessary***

If we cannot maintain life support, we don't keep on living.

### Positive Actions

#### Levels
