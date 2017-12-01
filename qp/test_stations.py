"""Test the station module."""
from unittest import TestCase
from stations import Cockpit, AutoTurret, Shields, LifeSupport, STATIONS, \
    Engines, TargetingComputer, TractorBeam, Maintenance
from qp import STATS


class BaseStationTests(object):
    """Test all base stations."""

    def __init__(self, stat, base, boost, type):
        """Construct Base Station Base Test Cases."""
        self.__stat = stat
        self.__base = base
        self.__boost = boost
        self.__type = type

    def setUp(self):
        """Setup."""
        self.undertest = self.__type()

    def test_should_exist_in_stations_constant(self):
        """The station should boost the expected stat."""
        self.assertIsInstance(STATIONS[self.__type().id], self.__type)

    def test_should_return_stat(self):
        """The station should boost the expected stat."""
        self.assertIn(self.__stat, self.undertest.handle(False))

    def test_should_return_base_value(self):
        """The station should boost the expected stat with the base value."""
        self.assertDictContainsSubset(
            {self.__stat: self.__base},
            self.undertest.handle(False))

    def test_should_return_non_0_base_value(self):
        """A unboosted station should return a value greater than 0."""
        self.assertGreater(self.undertest.handle(False)[self.__stat], 0)

    def test_should_return_boosted_value(self):
        """A boosted station should apply the boost value."""
        self.assertDictContainsSubset(
            {self.__stat: self.__base + self.__base * self.__boost},
            self.undertest.handle(True))

    def test_should_return_non_0_boosted_value(self):
        """A unboosted station should return a value greater than 0."""
        self.assertGreater(self.undertest.handle(True)[self.__stat], 0)

    def test_boosted_is_greater_than_base(self):
        """A unboosted station should return a value greater than 0."""
        self.assertGreater(
            self.undertest.handle(True)[self.__stat],
            self.undertest.handle(False)[self.__stat])


class AutoTurretTests(BaseStationTests, TestCase):
    """Test AutoTurret."""

    def __init__(self, *args, **kwargs):
        """Pass in AutoTurret values."""
        super(AutoTurretTests, self).__init__(
            STATS.ATTACK_POWER, AutoTurret.BASE_VALUE, AutoTurret.BOOST_MOD,
            AutoTurret
        )
        TestCase.__init__(self, *args, **kwargs)


class CockpitTests(BaseStationTests, TestCase):
    """Test Cockpit Station."""

    def __init__(self, *args, **kwargs):
        """Pass in Cockpit values."""
        super(CockpitTests, self).__init__(
            STATS.DODGE, Cockpit.BASE_VALUE, Cockpit.BOOST_MOD, Cockpit
        )
        TestCase.__init__(self, *args, **kwargs)


class LifeSupportTests(BaseStationTests, TestCase):
    """Test Life Support Station."""

    def __init__(self, *args, **kwargs):
        """Pass in LifeSupport values."""
        super(LifeSupportTests, self).__init__(
            STATS.LIFE_SUPPORT, LifeSupport.BASE_VALUE, LifeSupport.BOOST_MOD,
            LifeSupport
        )
        TestCase.__init__(self, *args, **kwargs)


class ShieldsTests(BaseStationTests, TestCase):
    """Test Shields Station."""

    def __init__(self, *args, **kwargs):
        """Pass in Shields values."""
        super(ShieldsTests, self).__init__(
            STATS.SHIELD, Shields.BASE_VALUE, Shields.BOOST_MOD, Shields
        )
        TestCase.__init__(self, *args, **kwargs)


class EnginesTests(BaseStationTests, TestCase):
    """Test Engines Station."""

    def __init__(self, *args, **kwargs):
        """Pass in Engines values."""
        super(EnginesTests, self).__init__(
            STATS.WARP, Shields.BASE_VALUE, Shields.BOOST_MOD, Engines
        )
        TestCase.__init__(self, *args, **kwargs)


class TractorBeamTests(BaseStationTests, TestCase):
    """Test Tractor Beam Station."""

    def __init__(self, *args, **kwargs):
        """Pass in TractorBeam values."""
        super(TractorBeamTests, self).__init__(
            STATS.INTERCEPT, Shields.BASE_VALUE, Shields.BOOST_MOD, TractorBeam
        )
        TestCase.__init__(self, *args, **kwargs)


class TargetingComputerTests(BaseStationTests, TestCase):
    """Test TargetingComputer Station."""

    def __init__(self, *args, **kwargs):
        """Pass in TargetingComputer values."""
        super(TargetingComputerTests, self).__init__(
            STATS.ACCURACY, Shields.BASE_VALUE,
            Shields.BOOST_MOD, TargetingComputer
        )
        TestCase.__init__(self, *args, **kwargs)


class MaintenanceTests(BaseStationTests, TestCase):
    """Test Maintenance Station."""

    def __init__(self, *args, **kwargs):
        """Pass in Maintenance values."""
        super(MaintenanceTests, self).__init__(
            STATS.HULL_HEALTH, Shields.BASE_VALUE,
            Shields.BOOST_MOD, Maintenance
        )
        TestCase.__init__(self, *args, **kwargs)
