"""Cockpit Station."""
from .base_station import BaseStation
from .. qp_constants import STATS


class Cockpit(BaseStation):
    """Cockpit Station.

    Working: Provides X to D.
    Manned: Provides additional D by X%.
    Damaged: Provides nothing. Cannot Warp.
    """

    BASE_VALUE = 1  # TODO
    BOOST_MOD = 1  # TODO

    def __init__(self):
        """Construct a Cockpit."""
        super(Cockpit, self). \
            __init__(STATS.DODGE, self.BASE_VALUE, self.BOOST_MOD)
