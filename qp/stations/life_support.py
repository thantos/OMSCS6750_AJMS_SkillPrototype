"""Life Support Station."""
from .base_station import BaseStation
from .. qp_constants import STATS


class LifeSupport(BaseStation):
    """Life Support Station.

    Working: Provides X to LS.
    Manned: Provides additional X% to LS.
    Damaged: Provides nothing. (LS will decrease by LSD)
    """

    BASE_VALUE = 1  # TODO
    BOOST_MOD = 1  # TODO

    def __init__(self):
        """Construct a Cockpit."""
        super(LifeSupport, self). \
            __init__(STATS.LIFE_SUPPORT, self.BASE_VALUE, self.BOOST_MOD)
