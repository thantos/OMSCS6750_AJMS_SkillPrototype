"""Maintenance Station."""
from .base_station import BaseStation
from .. qp_constants import STATS


class Maintenance(BaseStation):
    """Maintenance Station.

    Working: Provides X M.
    Manned: Provides additional X M.
    Damaged: Provides nothing.
    """

    BASE_VALUE = 1  # TODO
    BOOST_MOD = 1  # TODO

    def __init__(self):
        """Construct a Maintenance Station."""
        super(Maintenance, self). \
            __init__(
                "MAINTENANCE", "Maintenance", STATS.HULL_HEALTH,
                self.BASE_VALUE, self.BOOST_MOD)
