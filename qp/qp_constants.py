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
    STATION_FIRE_CHANCE = .7  # TODO
    STATION_DAMAGE_CHANCE = .4  # TODO
    LIFE_SUPPORT_DECAY = 15  # TODO <0
    BASE_WARP_THRESHOLD = None  # TODO >0


"""Stat values used by all players."""
BASE_STATS = {
    STATS.MAX_HULL_HEALTH: 100,  # TODO
    STATS.MAX_LS: 100,  # TODO
    STATS.ACCURACY: 4
}


STARTING_STATIONS = ["AUTO_TURRET", "COCKPIT", "LIFE_SUPPORT"]  # , "ENGINES"]


class EndGameState(object):
    """Object representing a end game senerio."""

    def __init__(self, player_loss, name):
        """Build end game state."""
        self.player_loss = player_loss
        self.name = name


class END_GAME_STATES(object):
    """Collection of possible ways to end combat."""

    PLAYER_HULL_DESTROYED = EndGameState(True, "Player hull destroyed")
    PLAYER_LIFE_SUPPORT_LOSS = EndGameState(True, "Player life support loss")
    OPPONENT_HULL_DESTROYED = EndGameState(False, "Opponent hull destroyed")


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
