"""Life Support Station."""
from .base_station import BaseStation
from .. qp_constants import STATS


class LifeSupport(BaseStation):
    """Life Support Station.

    Working: Provides X to LS.
    Manned: Provides additional X% to LS.
    Damaged: Provides nothing. (LS will decrease by LSD)
    """

    BASE_VALUE = 15  # TODO
    BOOST_MOD = 15  # TODO

    def __init__(self):
        """Construct a Cockpit."""
        super(LifeSupport, self). \
            __init__(
                "LIFE_SUPPORT", "Life Support", STATS.LS_CHARGE,
                self.BASE_VALUE, self.BOOST_MOD)
