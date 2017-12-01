"""QP Runner Module."""
from qp import QPEngine, CONSTANTS, STATS, STARTING_STATIONS, CREW_MEMBERS
from state import QPGameState, Ship, StationState, StageState, \
    CrewMemberState, EnemyState
import random


class QPRunner(object):
    """Logic for playing a game of QP."""

    def __init__(self):
        """Build new QP Runner."""
        self.engine = QPEngine()

    def new_game(self):
        """Create empty game state with no stage."""
        # TODO add other starting stations
        return QPGameState(Ship(
                {station: StationState()
                    for station in STARTING_STATIONS},
                {crew: CrewMemberState()
                    for crew in random.sample(
                    CREW_MEMBERS.keys(),
                    CONSTANTS.STARTING_CREW_MEMBERS)},
                {}),  # Leave stats empty for now
            None)

    def start_stage(self, stage_name):
        """Get a clean instance of a stage."""
        # TODO make more stages and a way to load them
        return StageState(EnemyState("Destroyer", {
            STATS.HULL_HEALTH: 10,
            STATS.ATTACK_POWER: 1,
            STATS.ACCURACY: .5,
            STATS.DODGE: 0,
            STATS.SHIELD: 0
        }))

    def advance_combat(self, game_state):
        # TODO is this the dict or the object game state?
        new_state = self.engine.advance(game_state)

        end_game = self.engine.check_for_endgame_states(new_state)

        return (new_state, end_game)

    def instruct_crew(self, game_state, crew, station):
        return self.engine.instruct_crew(game_state, crew, station)
