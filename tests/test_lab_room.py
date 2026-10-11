import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.lab_room import LabRoom
from models.computer import Computer
from models.printer import Printer, NetworkPrinter
from models.projector import Projector
from models.device import DeviceStatus


def make_computer(device_id="C01", year=2022):
    return Computer(device_id, f"PC {device_id}", year, 10000000, 8, "Intel i5", False)


def make_printer(device_id="P01"):
    return Printer(device_id, f"Printer {device_id}", 2022, 5000000, "laser", 50000, False)


class TestLabRoomInit(unittest.TestCase):
    def test_valid_init(self):
        room = LabRoom("R01", "Phòng A", 30)
        self.assertEqual(room.room_id, "R01")
        self.assertEqual(room.room_name, "Phòng A")
        self.assertEqual(room.capacity, 30)
        self.assertEqual(room.devices, [])

    def test_room_id_read_only(self):
        room = LabRoom("R01", "Phòng A", 30)
        with self.assertRaises(AttributeError):
            room.room_id = "R99"

    def test_empty_room_id_raises(self):
        with self.assertRaises(ValueError):
            LabRoom("", "Phòng A", 30)

    def test_whitespace_room_id_raises(self):
        with self.assertRaises(ValueError):
            LabRoom("  ", "Phòng A", 30)

    def test_empty_room_name_raises(self):
        with self.assertRaises(ValueError):
            LabRoom("R01", "", 30)

    def test_zero_capacity_raises(self):
        with self.assertRaises(ValueError):
            LabRoom("R01", "Phòng A", 0)

    def test_negative_capacity_raises(self):
        with self.assertRaises(ValueError):
            LabRoom("R01", "Phòng A", -5)

    def test_init_with_devices_list(self):
        c = make_computer("C01")
        p = make_printer("P01")
        room = LabRoom("R01", "Phòng A", 30, devices=[c, p])
        self.assertEqual(len(room.devices), 2)


class TestLabRoomAddDevice(unittest.TestCase):
    def setUp(self):
        self.room = LabRoom("R01", "Phòng A", 30)

    def test_add_single_device(self):
        self.room.add_device(make_computer("C01"))
        self.assertEqual(len(self.room.devices), 1)

    def test_add_multiple_devices(self):
        self.room.add_device(make_computer("C01"))
        self.room.add_device(make_printer("P01"))
        self.assertEqual(len(self.room.devices), 2)

    def test_add_duplicate_id_raises(self):
        self.room.add_device(make_computer("C01"))
        with self.assertRaises(ValueError):
            self.room.add_device(make_computer("C01"))

    def test_add_none_raises(self):
        with self.assertRaises((ValueError, TypeError, AttributeError)):
            self.room.add_device(None)

    def test_add_non_device_raises(self):
        with self.assertRaises((ValueError, TypeError, AttributeError)):
            self.room.add_device("not a device")


class TestLabRoomRemoveDevice(unittest.TestCase):
    def setUp(self):
        self.room = LabRoom("R01", "Phòng A", 30)
        self.room.add_device(make_computer("C01"))
        self.room.add_device(make_printer("P01"))

    def test_remove_existing_device_returns_true(self):
        result = self.room.remove_device("C01")
        self.assertTrue(result)

    def test_remove_existing_device_reduces_count(self):
        self.room.remove_device("C01")
        self.assertEqual(len(self.room.devices), 1)

    def test_remove_nonexistent_device_returns_false(self):
        result = self.room.remove_device("XXXX")
        self.assertFalse(result)

    def test_remove_does_not_affect_other_devices(self):
        self.room.remove_device("C01")
        self.assertIsNotNone(self.room.find_device("P01"))


class TestLabRoomFindDevice(unittest.TestCase):
    def setUp(self):
        self.room = LabRoom("R01", "Phòng A", 30)
        self.computer = make_computer("C01")
        self.room.add_device(self.computer)

    def test_find_existing_device(self):
        found = self.room.find_device("C01")
        self.assertIs(found, self.computer)

    def test_find_nonexistent_device_returns_none(self):
        result = self.room.find_device("XXXX")
        self.assertIsNone(result)


class TestLabRoomDevicesImmutability(unittest.TestCase):
    def test_devices_returns_copy(self):
        room = LabRoom("R01", "Phòng A", 30)
        room.add_device(make_computer("C01"))
        copy = room.devices
        copy.clear()
        self.assertEqual(len(room.devices), 1)


class TestLabRoomStr(unittest.TestCase):
    def test_str_contains_room_id(self):
        room = LabRoom("R01", "Phòng A", 30)
        self.assertIn("R01", str(room))

    def test_str_contains_room_name(self):
        room = LabRoom("R01", "Phòng A", 30)
        self.assertIn("Phòng A", str(room))


if __name__ == "__main__":
    unittest.main()
