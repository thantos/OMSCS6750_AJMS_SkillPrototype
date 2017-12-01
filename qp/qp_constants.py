"""Base Constants for Quick Particle."""


class STATS(object):
    """Stats used by QP."""

    ATTACK_POWER = "Attack Power"
    ACCURACY = "Accuracy"
    DODGE = "Dodge"
    SHIELD = "Shield"
    WARP = "Warp"
    INTERCEPT = "Intercept"
    LIFE_SUPPORT = "Life Support"
    LS_CHARGE = "Life Support Charge"
    MAX_LS = "Max Life Support"
    HULL_HEALTH = "Hull Health"
    MAX_HULL_HEALTH = "MAX Hull Health"


class STAT_CONSTANTS(object):
    """Constants used by QP."""

    FIRE_SUPPRESSION = 2
    STATION_FIRE_CHANCE = None  # TODO
    STATION_DAMAGE_CHANCE = None  # TODO
    LIFE_SUPPORT_DECAY = None  # TODO <0
    BASE_WAP_LEVEL = None  # TODO >0


"""Stat values used by all players."""
BASE_STATS = {
    STATS.MAX_HULL_HEALTH: 10,  # TODO
    STATS.MAX_LS: 10  # TODO
}


STARTING_STATIONS = ["AUTO_TURRET", "COCKPIT", "LIFE_SUPPORT", "ENGINES"]


class EndGameState(object):
    """Object representing a end game senerio."""

    def __init__(self, player_loss):
        """Build end game state."""
        self.player_loss = player_loss


class END_GAME_STATES(object):
    """Collection of possible ways to end combat."""

    PLAYER_HULL_DESTROYED = EndGameState(True)
    PLAYER_LIFE_SUPPORT_LOSS = EndGameState(True)
    OPPONENT_HULL_DESTROYED = EndGameState(False)


CREW_MEMBERS = {
    "AMY": {
        "name": "Amy",
        "id": "AMY"
    },
    "JERRI": {
        "name": "Jerri",
        "id": "JERRI"
    },
    "LESTER": {
        "name": "Lester",
        "id": "LESTER"
    },
    "MICK": {
        "name": "Mick",
        "id": "MICK"
    },
    "SAM": {
        "name": "Sam",
        "id": "SAM"
    }
}


class CONSTANTS(object):
    """Misc constants."""

    STARTING_CREW_MEMBERS = 2
