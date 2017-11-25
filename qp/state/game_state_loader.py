"""Game State Loader."""
from .qp_game_state import QPGameState, CrewMemberState, Ship, StationState, \
    StageState, EnemyState


class GameStateLoader(object):
    """Hydrates the game state object from a dictionary."""

    def __init__(self):
        """Build the loader."""
        pass

    def loadGameState(self, game_state):
        """Load the game state from a dictionary to an object."""
        return QPGameState(
                self.__getShip(game_state.get('ship', None)),
                self.__getStage(game_state.get('stage', None)))

    def __getShip(self, ship):
        """Build ship.

        If ship is None, raise error.
        If  stations is missing, raise error. There should always at least one
        Station.
        If crew is missing, raise error. There should always be at least one
        crew member.
        If stats is missing, return empty collection.
        """
        if ship is None:
            raise ValueError("Ship is required")
        station_dict = ship.get('stations')
        if station_dict is None:
            raise ValueError("Stations should not be empty")
        stations = {key: self.__getStation(station)
                    for key, station in station_dict.iteritems()}
        crew_dict = ship.get('crew')
        if crew_dict is None:
            raise ValueError("Crew should not be empty")
        crew = {name: CrewMemberState(crew.get('station'))
                for name, crew in crew_dict.iteritems()}

        return Ship(stations, crew, ship.get('stats', {}))

    def __getStation(self, station):
        return StationState() if station is None \
            else StationState(
                station.get('fire', 0), station.get('damaged', False))

    def __getStage(self, stage):
        """Build the stage.

        If no stage is present, return None.
        """
        if stage is None:
            return None
        opp = stage.get('opponent')
        if opp is None:
            return StageState()
        return StageState(self.__getEnemyState(opp))

    def __getEnemyState(self, opponent):
        return EnemyState(opponent.get('name'), opponent.get('stats', {}))
