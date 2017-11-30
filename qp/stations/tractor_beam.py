"""Tractor Beam Station."""
from .base_station import BaseStation
from .. qp_constants import STATS


class TractorBeam(BaseStation):
    """Tractor Beam Station.

    Working: Provides X I.
    Manned: Provides additional X% I.
    Damaged: Provides nothing.
    """

    BASE_VALUE = 1  # TODO
    BOOST_MOD = 1  # TODO

    def __init__(self):
        """Construct a Tractor Beam Station."""
        super(TractorBeam, self). \
            __init__(
                "TRACTOR_BEAM", "Tractor Beam", STATS.INTERCEPT,
                self.BASE_VALUE, self.BOOST_MOD)
