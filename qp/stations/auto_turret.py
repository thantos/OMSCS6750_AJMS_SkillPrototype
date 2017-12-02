"""Auto Turret Station."""
from .base_station import BaseStation
from .. qp_constants import STATS


class AutoTurret(BaseStation):
    """Auto Turret Station.

    TODO Change attacking to be based on damage range instead of flat damage.

    Working: Provides X to P.
    Manned: Provides additional P by X%.
    Damaged: Provides nothing.
    """

    BASE_VALUE = 5  # TODO
    BOOST_MOD = 5  # TODO

    def __init__(self):
        """Construct a Cockpit."""
        super(AutoTurret, self). \
            __init__(
                "AUTO_TURRET", "Auto Turret", STATS.ATTACK_POWER,
                self.BASE_VALUE, self.BOOST_MOD)
