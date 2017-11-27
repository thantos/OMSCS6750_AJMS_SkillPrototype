"""Quick Prticle Custom Exceptions."""


class CrewMemberInvalidException(Exception):
    """Throw when a crew member name given doesn't exist."""

    pass


class StationInvalidException(Exception):
    """Throw when a station targeted doesn't exist."""

    pass


class MemberAlreadyInStationException(Exception):
    """Thrown when a member is moved to a station they are already at."""

    pass
