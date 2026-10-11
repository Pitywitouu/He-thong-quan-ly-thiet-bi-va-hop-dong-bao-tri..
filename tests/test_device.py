import sys
import os
import unittest
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.device import DeviceStatus
from models.computer import Computer


class TestDeviceStatusEnum(unittest.TestCase):
    def test_active_value(self):
        self.assertEqual(DeviceStatus.ACTIVE.value, "Active")

    def test_under_maintenance_value(self):
        self.assertEqual(DeviceStatus.UNDER_MAINTENANCE.value, "UnderMaintenance")

    def test_retired_value(self):
        self.assertEqual(DeviceStatus.RETIRED.value, "Retired")

    def test_alias_active(self):
        self.assertEqual(DeviceStatus.Active, DeviceStatus.ACTIVE)

    def test_alias_under_maintenance(self):
        self.assertEqual(DeviceStatus.UnderMaintenance, DeviceStatus.UNDER_MAINTENANCE)


class TestDeviceInit(unittest.TestCase):
    def _make(self, **kwargs):
        defaults = dict(
            device_id="D01", name="Test PC", year_in_use=2022,
            purchase_price=10000000, ram=8, processor_type="Intel i5",
            has_discrete_gpu=False
        )
        defaults.update(kwargs)
        return Computer(**defaults)

    def test_valid_init(self):
        d = self._make()
        self.assertEqual(d.device_id, "D01")
        self.assertEqual(d.name, "Test PC")
        self.assertEqual(d.year_in_use, 2022)
        self.assertAlmostEqual(d.purchase_price, 10000000.0)
        self.assertEqual(d.status, DeviceStatus.ACTIVE)

    def test_default_status_is_active(self):
        d = self._make()
        self.assertEqual(d.status, DeviceStatus.ACTIVE)

    def test_custom_status(self):
        d = self._make(status=DeviceStatus.RETIRED)
        self.assertEqual(d.status, DeviceStatus.RETIRED)

    def test_strips_whitespace_device_id(self):
        d = self._make(device_id="  D01  ")
        self.assertEqual(d.device_id, "D01")

    def test_strips_whitespace_name(self):
        d = self._make(name="  My PC  ")
        self.assertEqual(d.name, "My PC")


class TestDeviceIdReadOnly(unittest.TestCase):
    def test_device_id_read_only(self):
        d = Computer("D01", "PC", 2022, 10000000, 8, "Intel i5", False)
        with self.assertRaises(AttributeError):
            d.device_id = "D99"


class TestDeviceValidation(unittest.TestCase):
    def _make(self, **kwargs):
        defaults = dict(
            device_id="D01", name="Test PC", year_in_use=2022,
            purchase_price=10000000, ram=8, processor_type="Intel i5",
            has_discrete_gpu=False
        )
        defaults.update(kwargs)
        return Computer(**defaults)

    def test_empty_device_id_raises(self):
        with self.assertRaises(ValueError):
            self._make(device_id="")

    def test_whitespace_device_id_raises(self):
        with self.assertRaises(ValueError):
            self._make(device_id="   ")

    def test_empty_name_raises(self):
        with self.assertRaises(ValueError):
            self._make(name="")

    def test_whitespace_name_raises(self):
        with self.assertRaises(ValueError):
            self._make(name="   ")

    def test_future_year_raises(self):
        future = datetime.now().year + 1
        with self.assertRaises(ValueError):
            self._make(year_in_use=future)

    def test_zero_year_raises(self):
        with self.assertRaises(ValueError):
            self._make(year_in_use=0)

    def test_negative_year_raises(self):
        with self.assertRaises(ValueError):
            self._make(year_in_use=-5)

    def test_zero_price_raises(self):
        with self.assertRaises(ValueError):
            self._make(purchase_price=0)

    def test_negative_price_raises(self):
        with self.assertRaises(ValueError):
            self._make(purchase_price=-1000)

    def test_invalid_status_string_raises(self):
        with self.assertRaises((ValueError, KeyError)):
            self._make(status="INVALID_STATUS")

    def test_invalid_status_type_raises(self):
        with self.assertRaises(TypeError):
            self._make(status=123)


class TestDeviceYearsOfUse(unittest.TestCase):
    def test_years_of_use_positive(self):
        d = Computer("D01", "PC", 2019, 10000000, 8, "Intel i5", False)
        self.assertGreater(d.years_of_use, 0)

    def test_years_of_use_current_year(self):
        current = datetime.now().year
        d = Computer("D01", "PC", current, 10000000, 8, "Intel i5", False)
        self.assertEqual(d.years_of_use, 0)

    def test_years_of_use_calculation(self):
        d = Computer("D01", "PC", 2020, 10000000, 8, "Intel i5", False)
        expected = datetime.now().year - 2020
        self.assertEqual(d.years_of_use, expected)


class TestDeviceStr(unittest.TestCase):
    def test_str_contains_id(self):
        d = Computer("D01", "MyPC", 2022, 10000000, 8, "Intel i5", False)
        self.assertIn("D01", str(d))

    def test_str_contains_name(self):
        d = Computer("D01", "MyPC", 2022, 10000000, 8, "Intel i5", False)
        self.assertIn("MyPC", str(d))

    def test_repr_contains_class_name(self):
        d = Computer("D01", "MyPC", 2022, 10000000, 8, "Intel i5", False)
        self.assertIn("Computer", repr(d))


if __name__ == "__main__":
    unittest.main()
