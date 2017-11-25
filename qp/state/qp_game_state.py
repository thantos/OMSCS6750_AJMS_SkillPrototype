
"""Game State Module."""


class QPGameState(object):
    """State which is maintained and modified throughout a game session."""

    def __init__(self, ship, stage):
        """Build QP Game State.

        ship  -- Ship, Player's ship. Required.
        stage -- StageState, Information about the current stage, like opponent
                 and environment.
        """
        if ship is None:
            raise ValueError("Ship must be present.")
        self.ship = ship
        self.stage = stage


class Ship(object):
    """Represents a player object which is manipulated and returned.

    stations -- Dict[String, StationState], Dict of station name to
                StationState. Required.
    stats    -- Dict[String, Integer], Dict of stat to value.
                Should be persistant and base values, like hull health
    crew     -- CrewMemeberState, A list of crew members. Required.
    """

    def __init__(self, stations, crew, stats={}):
        """Build player."""
        if stations is None or crew is None:
            raise ValueError("Stations and Crew must be present.")
        self.stations = stations
        self.stats = stats
        self.crew = crew


class StationState(object):
    """State of a station.

    A station can be damaged or on fire.
    Note: A station can also be manned,
    but that will be stored in the crew state.
    """

    def __init__(self, fire=0, damanged=False):
        """Build Station State.

        fire    -- Integer, Number of turns the has been present.
                   Default is 0.
        damaged -- Boolean, whether or not the station is damaged.
                   Default is False.
        """
        self.fire = fire
        self.damaged = damanged


class CrewMemberState(object):
    """Represents a crew member's current state."""

    def __init__(self, station=None):
        """Build station.

        station -- String, Name of the station the crew member is at.
        """
        self.station = station


class StageState(object):
    """The state of the stage the player is on."""

    def __init__(self, opponent=None):
        """Build the stage.

        opponent -- EnemyState, Enemy which the player is facing.
                    TODO make the enemy a regular player ship instead of static
                    stats.
        """
        self.opponent = opponent


class EnemyState(object):
    """The opponent the player is facing."""

    def __init__(self, name, stats):
        """Build an EnemyState.

        name  -- String, Opponent name to use in TTS.
        stats -- Dict[String, Integer], Dict of stat name to value.
        """
        self.stats = stats
        self.name = name
