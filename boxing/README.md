# Alexa Boxing Coach (needs name)


![](https://snescentral.com/0/9/1/0913/screen03.png)

## Premise

You are a boxing coach sitting in your boxer's corner of the ring. You are responsible for calling out strategies to the boxer, anticipating opponent patterns, and helping your boxer win the fight. Alexa is a flamboyant announcer that keeps track of the state of the game and describes the action.


## Game Structure

The game plays out over 3 rounds. Each round is comprised of a set of turns. The number of turns per round is drawn at random from a normal distribution. Every turn each boxer performs one move. Some percent of the time the boxer will act of their own accord and pick actions based on what their coach has told them so far.

### How to win

To win the game the player can knockout their opponent or win by decision. The decision is based on who landed more punches or more high quality punches. Punch quality is discussed below.

### Game state

Each boxer has two main stats: Health Points (HP) and Stamina. The various moves each boxer can make can change these two stats.

### Manuevers

The coach can call out one of a set number of 'moves' for the boxer. These are broken into three types: Offensive, Defensive and Neutral. Defensive maneuvers can increase the players HP and stamina while making it harder to hit them. Offensive maneuvers can decrease the opponents HP and/or Stamina but requires some stamina to perform. Neutral maneuvers are ways to add a temporary bonus to the next move if pulled off successfully.

### Offensive Moves
* Jab - Simple shot to the body/head
* Hook - More difficult head shot
* Cross - Powerful straight shot
* Upper Cut - Dramatic, Powerful shot

### Defensive Moves
* Bob and weave - move the body not the feet
* Foot work - dance back and forth
* Protect the body - Boxer positions arms in front of their core
* Hands up - Boxer moves the gloves in front of their face

### Neutral Moves
* Taunt - Openly mock the other boxer
* Wrap up - Try to grapple the other boxer
* Feint - Pretend to throw a punch

### Special Moves
Certain combos and add temporary bonus stats for players
Certain punches are only possible when successfully executing combos
