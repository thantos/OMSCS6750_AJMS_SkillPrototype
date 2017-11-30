"""Quick Particle Stations Module."""
from .auto_turret import AutoTurret
from .cockpit import Cockpit
from .life_support import LifeSupport
from .shields import Shields
from .maintenance import Maintenance
from .engines import Engines
from .targeting_computer import TargetingComputer
from .tractor_beam import TractorBeam

__station_clases = [AutoTurret, Cockpit, LifeSupport, Shields,
                    Maintenance, TractorBeam, Engines, TargetingComputer]

"""Dictionary of station classes."""
STATIONS = {s.id: s for s in [station() for station in __station_clases]}

__all__ = ['STATIONS']
