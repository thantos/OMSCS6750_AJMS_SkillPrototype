"""Auto Turret Station."""
from .base_station import BaseStation
from .. qp_constants import STATS


class AutoTurret(BaseStation):
    """Auto Turret Station.

    Working: Provides X to P.
    Manned: Provides additional P by X%.
    Damaged: Provides nothing.
    """

    BASE_VALUE = 0  # TODO
    BOOST_MOD = 1  # TODO

    def __init__(self):
        """Construct a Cockpit."""
        super(AutoTurret, self). \
            __init__(STATS.ATTACK_POWER, self.BASE_VALUE, self.BOOST_MOD)
