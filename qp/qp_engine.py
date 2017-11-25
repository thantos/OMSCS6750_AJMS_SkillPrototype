"""Game Engine for Quick Particle."""
import stations
from state import GameStateLoader


class QPEngine(object):
    """Quick Particle Game Engine.

    This class should be stateless.
    """

    def __init__(self):
        """Construct new game engine instance."""
        self.stateLoader = GameStateLoader()

    def advance(self, game_state):
        """Advance Time by one Turn

        Report Current State
        Player Commands Crew.
        Update Stats based on new Position
        Combat
        Apply Tasks
        Repair/Fire Suppression
        Apply Combat Impacts
        Check for End Game States
        Repeat @ 1
        """
        # Game state comes in as a dictionary, turn it into a GameState object
        state = self.stateLoader.loadGameState(game_state)
