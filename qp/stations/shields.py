"""Shields Station."""
from .base_station import BaseStation
from .. qp_constants import STATS


class Shields(BaseStation):
    """Shields Station.

    Working: Provides X S.
    Manned: Provides additional S by X%.
    Damaged: Provides nothing.
    """

    BASE_VALUE = 1  # TODO
    BOOST_MOD = 1  # TODO

    def __init__(self):
        """Construct a Cockpit."""
        super(Shields, self). \
            __init__(STATS.SHIELD, self.BASE_VALUE, self.BOOST_MOD)
