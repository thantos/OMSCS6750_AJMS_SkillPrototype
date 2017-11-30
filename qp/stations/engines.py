"""Engines Station."""
from .base_station import BaseStation
from .. qp_constants import STATS


class Engines(BaseStation):
    """Engines Station.

    Working: Provides X W/turn.
    Manned: Provides additional X% W/turn.
    Damaged: Provides nothing. Cannot Warp.
    """

    BASE_VALUE = 1  # TODO
    BOOST_MOD = 1  # TODO

    def __init__(self):
        """Construct a Engine Station."""
        super(Engines, self). \
            __init__(
                "ENGINES", "Engines", STATS.WARP,
                self.BASE_VALUE, self.BOOST_MOD)
