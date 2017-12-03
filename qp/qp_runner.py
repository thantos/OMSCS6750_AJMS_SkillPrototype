"""QP Runner Module."""
from qp import QPEngine, STATS, CREW_MEMBERS
from state import QPGameState, Ship, StationState, StageState, \
    CrewMemberState, EnemyState, GameStateLoader
from stations import STATIONS
import random
from copy import deepcopy


class QPRunner(object):
    """Logic for playing a game of QP."""

    def __init__(self):
        """Build new QP Runner."""
        self.engine = QPEngine()
        self.__state_loader = GameStateLoader()

    def new_game(self, number_of_crew, starting_stations):
        """Create empty game state with no stage."""
        # TODO add other starting stations
        return QPGameState(Ship(
                {station: StationState()
                    for station in starting_stations},
                {crew: CrewMemberState()
                    for crew in random.sample(
                    CREW_MEMBERS.keys(),
                    number_of_crew)},
                {}),  # Leave stats empty for now
            None)

    def start_stage(self, opponent_name, opponent_stats):
        """Get a clean instance of a stage."""
        # TODO make more stages and a way to load them
        return StageState(EnemyState(opponent_name, opponent_stats))

    def prime_ship_for_combat(self, stats):
        """Set the required stage persistent stats.

        Set hull health to the max value
        Set life support to the max value
        Prime warp to 0
        """
        new_stats = deepcopy(stats)
        new_stats[STATS.HULL_HEALTH] = stats.get(STATS.MAX_HULL_HEALTH)
        new_stats[STATS.LIFE_SUPPORT] = stats.get(STATS.MAX_LS)
        new_stats[STATS.WARP] = 0

        return new_stats

    def advance_combat(self, game_state):
        """Execute a round of combat.

        Update the game state
        Report end games.
        """
        # TODO is this the dict or the object game state?
        (new_state, qp_results) = self.engine.advance(game_state)

        end_game = self.engine.check_for_endgame_states(new_state)

        return (new_state, end_game, qp_results)

    def instruct_crew(self, game_state, crew, station):
        """Command a crew member to a station.

        crew -- Crew ID from the skill slot id and the CREW_MEMBER constant.
        station -- Station ID from the skill slot id.
        """
        return (
            self.engine.instruct_crew(game_state, crew, station),
            CREW_MEMBERS[crew], STATIONS[station])

    def transform_game_state(self, game_state_dict):
        """Transform the game state dictionary into QPGameState."""
        return self.__state_loader.loadGameState(game_state_dict)

    def to_json_friendly(self, obj):
        if hasattr(obj, '__dict__'):
            return self.to_json_friendly(obj.__dict__)
        elif isinstance(obj, list):
            return [self.to_json_friendly(x) for x in list]
        elif isinstance(obj, dict):
            return {k: self.to_json_friendly(v) for (k, v) in obj.iteritems()}
        else:
            return obj
